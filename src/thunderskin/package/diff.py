from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.resource import Resource
from thunderskin.exceptions import UnreachableError


def diff(old: Package, new: Package) -> dict[str, list[Object | Resource]]:
    old_symbol_entry_map = {obj.symbol(): obj for obj in old.objects} | {
        res.symbol(): res for res in old.resources
    }
    new_symbol_entry_map = {obj.symbol(): obj for obj in new.objects} | {
        res.symbol(): res for res in new.resources
    }
    old_symbols = set(old_symbol_entry_map.keys())
    new_symbols = set(new_symbol_entry_map.keys())
    deleted_symbols = old_symbols - new_symbols
    newed_symbols = new_symbols - old_symbols
    common_symbols = old_symbols & new_symbols
    modified_symbols = {
        uid
        for uid in common_symbols
        if old_symbol_entry_map[uid] != new_symbol_entry_map[uid]
    }

    new_objs = [new_symbol_entry_map[uid] for uid in (newed_symbols | modified_symbols)]
    deleted_objs = [old_symbol_entry_map[uid] for uid in deleted_symbols]

    return {
        "new": sorted(new_objs, key=lambda x: x.symbol()),
        "delete": sorted(deleted_objs, key=lambda x: x.symbol()),
    }


def diff_list(packages: list[Package]) -> list[dict[str, list[Object | Resource]]]:
    return [diff(pkg_old, pkg_new) for pkg_old, pkg_new in zip(packages, packages[1:])]
