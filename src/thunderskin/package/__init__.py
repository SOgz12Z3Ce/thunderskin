from thunderskin.object import Object

from thunderskin.resource import Resource


class Package:
    def __init__(
        self, name: str, version: str, objects: list[Object], resources: list[Resource]
    ):
        self.name = name
        self.version = version
        self.objects = objects
        self.resources = resources
