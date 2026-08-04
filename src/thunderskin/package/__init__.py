from thunderskin.object import Object


class Package:
    def __init__(self, name: str, version: str, objects: list[Object]):
        self.name = name
        self.version = version
        self.objects = objects
