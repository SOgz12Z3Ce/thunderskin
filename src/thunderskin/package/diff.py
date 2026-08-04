from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.json.types import JsonObject
from thunderskin.exceptions import UnreachableError


def diff(old: Package, new: Package) -> JsonObject:
    old_unique_id_object_map = {obj.unique_id(): obj for obj in old.objects}
    new_unique_id_object_map = {obj.unique_id(): obj for obj in new.objects}
    old_unique_ids = set(old_unique_id_object_map.keys())
    new_unique_ids = set(new_unique_id_object_map.keys())
    deleted_unique_ids = list(old_unique_ids - new_unique_ids)
    newed_unique_ids = list(new_unique_ids - old_unique_ids)
    common_unique_ids = old_unique_ids & new_unique_ids
    modified_unique_ids = [
        uid
        for uid in common_unique_ids
        if old_unique_id_object_map[uid] != new_unique_id_object_map[uid]
    ]
    return {
        "new": sorted(newed_unique_ids + modified_unique_ids),
        "delete": sorted(deleted_unique_ids),
    }
