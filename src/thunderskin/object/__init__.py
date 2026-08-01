from thunderskin.types import JsonValue


class Object:
    def __init__(self, group: str, l10n: str, properties: dict[str, JsonValue]):
        self.group = group
        self.l10n = l10n
        self.properties = properties
