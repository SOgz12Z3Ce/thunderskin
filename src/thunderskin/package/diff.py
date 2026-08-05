from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.json.types import JsonObject
from thunderskin.exceptions import UnreachableError


def diff(old: Package, new: Package) -> JsonObject:
    old_symbol_entry_map = {obj.symbol(): obj for obj in old.objects} | {
        res.symbol(): res for res in old.resources
    }
    new_symbol_entry_map = {obj.symbol(): obj for obj in new.objects} | {
        res.symbol(): res for res in new.resources
    }
    old_symbols = set(old_symbol_entry_map.keys())
    new_symbols = set(new_symbol_entry_map.keys())
    deleted_symbols = list(old_symbols - new_symbols)
    newed_symbols = list(new_symbols - old_symbols)
    common_symbols = old_symbols & new_symbols
    modified_symbols = [
        uid
        for uid in common_symbols
        if old_symbol_entry_map[uid] != new_symbol_entry_map[uid]
    ]

    return {
        "new": sorted(newed_symbols + modified_symbols),
        "delete": sorted(deleted_symbols),
    }

def diff_list(packages: list[Package]) -> JsonObject:
    return [diff(pkg_old, pkg_new) for pkg_old, pkg_new in zip(packages, packages[1:])]
