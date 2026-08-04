from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.json.types import JsonObject
from thunderskin.exceptions import UnreachableError


def diff(old: Package, new: Package) -> JsonObject:
    old_key_entry_map = {obj.key(): obj for obj in old.objects} | {res.key(): res for res in old.resources}
    new_key_entry_map = {obj.key(): obj for obj in new.objects} | {res.key(): res for res in new.resources}
    old_keys = set(old_key_entry_map.keys())
    new_keys = set(new_key_entry_map.keys())
    deleted_keys = list(old_keys - new_keys)
    newed_keys = list(new_keys - old_keys)
    common_keys = old_keys & new_keys
    modified_keys = [
        uid for uid in common_keys if old_key_entry_map[uid] != new_key_entry_map[uid]
    ]

    return {
        "new": sorted(newed_keys + modified_keys),
        "delete": sorted(deleted_keys),
    }
