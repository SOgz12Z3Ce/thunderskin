from thunderskin.types import JsonValue


class Object:
    def __init__(self, group: str, properties: dict[str, JsonValue]):
        self.group = group
        self.properties = properties
