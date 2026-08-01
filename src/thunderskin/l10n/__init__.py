from thunderskin.object import Object
from thunderskin.l10n.registry import L10N_REGISTRY


class L10nObject:
    def __init__(self, objects: list[Object]):
        self.group = objects[0].group
        self.l10n_properties_map = {}
        for obj in objects:
            self.l10n_properties_map[obj.l10n] = obj.properties

    def as_l10n(self, l10n: str):
        core = self._core()
        l10n_obj = self.l10n_properties_map[l10n]
        return localize(core, l10n_obj, L10N_REGISTRY[core.group])

    def _core(self) -> Object:
        return self.l10n_properties_map["en"]


def localize(target, reference, registry):
    for key in target.keys():
        if key not in registry:
            continue
        if callable(registry[key]):
            target[key] = registry[key](target[key], reference[key])
        else:
            target[key] = localize(target[key], reference[key], registry[key])
    return target
