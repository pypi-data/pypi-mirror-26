import attr
import click
import json

from docker.errors import NotFound

from ..cli.tasks import Task
from ..exceptions import ImageNotFoundException, ImagePullFailure, BadConfigError


@attr.s
class ImageRepository:
    """
    A repository of available images for containers.

    Recommended use is internal-only by the plugins, do not use directly.
    """
    host = attr.ib()
    images = attr.ib(default=attr.Factory(dict))

    def list_images(self):
        """
        List all available images.
        """
        raise NotImplementedError()

    def add_image(self, image_name, version, image_hash):
        """
        Add a hash for a given image_name and version.

        This will update any existing hash for an image that was previously
        added to the image repository instance.
        """
        raise NotImplementedError()

    def image_versions(self, image_name):
        """
        Returns a dictionary of version name mapped to the image hash for a
        given image name. May return empty dictionary if there are no images.
        """
        # TODO: Expand to read all tags locally, not just a fixed list
        try:
            return {"latest": self.image_version(image_name, "latest")}
        except ImageNotFoundException:
            return {}

    def get_registry(self, app):
        """
        Given an app, returns the registry handler responsible for handling it
        (or None if it does not need a handler)
        """
        registry = app.containers.registry
        if registry is None:
            return None
        # Work out what plugin to use
        plugin_name, registry_data = registry.split(":", 1)
        # Call the plugin to log in/etc to the registry
        registry_plugins = app.get_catalog_items("registry")
        if plugin_name == "plain":
            # The "plain" plugin is a shortcut for "no plugin"
            return BasicRegistryHandler(app, registry_data)
        elif plugin_name in registry_plugins:
            return registry_plugins[plugin_name](app, registry_data)
        else:
            raise BadConfigError("No registry plugin for {} loaded".format(plugin_name))

    def pull_image_version(self, app, image_name, image_tag, parent_task, fail_silently=False):
        """
        Pulls the most recent version of the given image tag from remote
        docker registry.
        """

        assert isinstance(image_name, str)
        assert isinstance(image_tag, str)

        # The string "local" has a special meaning which means the most recent
        # local image of that name, so we skip the remote call/check.
        if image_tag == "local":
            if fail_silently:
                return None
            else:
                raise ImagePullFailure(
                    "Cannot pull a local image",
                    remote_name=None,
                    image_tag=image_tag
                )

        # See if the registry is willing to give us a URL (it's logged in)
        registry = self.get_registry(app)
        if registry:
            registry_url = registry.url(self.host)
        else:
            registry_url = None
        if registry_url is None:
            if fail_silently:
                return None
            else:
                raise ImagePullFailure(
                    "No registry configured",
                    remote_name=None,
                    image_tag=image_tag
                )

        task = Task(
            "Pulling remote image {}:{}".format(image_name, image_tag),
            parent=parent_task,
            progress_formatter=lambda x: "{} MB".format(x // (1024 ** 2)),
        )

        remote_name = "{registry_url}/{image_name}".format(
            registry_url=registry_url,
            image_name=image_name,
        )

        stream = self.host.client.pull(remote_name, tag=image_tag, stream=True)
        layer_status = {}
        current = None
        total = None
        for line in stream:
            if isinstance(line, bytes):
                line = line.decode("ascii")
            data = json.loads(line)
            if 'error' in data:
                task.finish(status="Failed", status_flavor=Task.FLAVOR_WARNING)
                if fail_silently:
                    return
                else:
                    raise ImagePullFailure(
                        data['error'],
                        remote_name=remote_name,
                        image_tag=image_tag
                    )
            elif 'id' in data:
                if data['status'].lower() == "downloading":
                    layer_status[data['id']] = data['progressDetail']

                elif "complete" in data['status'].lower() and data['id'] in layer_status:
                    layer_status[data['id']]['current'] = layer_status[data['id']]['total']

                if layer_status:
                    statuses = [x for x in layer_status.values()
                                if "current" in x and "total" in x]
                    current = sum(x['current'] for x in statuses)
                    total = sum(x['total'] for x in statuses)

                if total is not None:
                    task.update(progress=(current, total))

        task.finish(status="Done", status_flavor=Task.FLAVOR_GOOD)

        # Tag the remote image as the right name
        try:
            self.host.client.tag(
                remote_name + ":" + image_tag,
                image_name,
                tag=image_tag,
                force=True
            )
        except NotFound:
            if fail_silently:
                return
            else:
                raise ImagePullFailure(
                    'Failed to tag {}:{}'.format(remote_name, image_name),
                    remote_name=remote_name,
                    image_tag=image_tag
                )

    def image_version(self, image_name, image_tag):
        """
        Returns the Docker image hash of the requested image and tag, or
        raises ImageNotFoundException if it's not available on the host.
        """
        if image_tag == "local":
            image_tag = "latest"
        try:
            docker_info = self.host.client.inspect_image("{}:{}".format(image_name, image_tag))
            return docker_info['Id']
        except NotFound:
            # TODO: Maybe auto-build if we can?
            raise ImageNotFoundException(
                "Cannot find image {}:{}".format(image_name, image_tag),
                image=image_name,
                image_tag=image_tag,
            )

    def push_image_version(self, app, image_name, image_tag, parent_task):
        """
        Pushes the given image version up to the repository
        """

        assert isinstance(image_name, str)
        assert isinstance(image_tag, str)

        # The string "local" has a special meaning which means the most recent
        # local image of that name, so we skip the remote call/check.
        if image_tag == "local":
            raise ValueError("You cannot push the 'local' version")

        # See if the registry is willing to give us a URL (it's logged in)
        registry = self.get_registry(app)
        if registry:
            registry_url = registry.url(self.host)
        else:
            registry_url = None
        if registry_url is None:
            raise RuntimeError("No registry configured")

        task = Task(
            "Pushing image {}:{}".format(image_name, image_tag),
            parent=parent_task,
            progress_formatter=lambda x: "{} MB".format(x // (1024 ** 2)),
        )

        # Work out the name it needs to be and tag the image as that
        remote_name = "{registry_url}/{image_name}".format(
            registry_url=registry_url,
            image_name=image_name,
        )
        self.host.client.tag(
            image_name + ":" + "latest",
            remote_name,
            tag=image_tag,
            force=True
        )

        # Push it up
        stream = self.host.client.push(remote_name, tag=image_tag, stream=True)
        layer_status = {}
        current = None
        total = None
        for line in stream:
            if isinstance(line, bytes):
                line = line.decode("ascii")
            data = json.loads(line)
            if 'error' in data:
                task.finish(status="Failed", status_flavor=Task.FLAVOR_WARNING)
                raise RuntimeError("Push error: %r" % data['error'])
            elif 'id' in data:
                if data['status'].lower() == "pushing":
                    layer_status[data['id']] = data['progressDetail']
                elif "complete" in data['status'].lower() and data['id'] in layer_status:
                    layer_status[data['id']]['current'] = layer_status[data['id']]['total']
                if layer_status:
                    statuses = [x for x in layer_status.values()
                                if "current" in x and "total" in x]
                    current = sum(x['current'] for x in statuses)
                    total = sum(x['total'] for x in statuses)
                if total is not None:
                    task.update(progress=(current, total))
        task.finish(status="Done", status_flavor=Task.FLAVOR_GOOD)


class BasicRegistryHandler:
    """
    Handler for basic (normal Docker) image registries
    """

    def __init__(self, app, data):
        self.registry_url = data

    def url(self, host):
        return self.registry_url

    def login(self, host, task):
        click.echo("Registry does not need a login")

    def logout(self, host, task):
        click.echo("Registry does not need a login")
