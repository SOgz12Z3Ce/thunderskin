from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.resource import Resource
from thunderskin.wiki.escape import escape
from thunderskin.json.types import JsonObject


def title(package: Package, entry: Object) -> str:
    return escape(f"{package.name}/{package.version}/{entry.symbol()}")


def diff_list_to_lua(
    diff_list: list[dict[str, list[Object | Resource]]], versions: list[str]
) -> str:
    res = ["local diff = {"]
    counter = 0
    reversed_versions = list(reversed(versions))
    for diff in reversed(diff_list):
        diff_lua = ["{"]
        diff_lua.append(f"version = '{reversed_versions[counter]}',")
        diff_lua.append("new = {")
        for entry in diff["new"]:
            if isinstance(entry, Object):
                if "label" in entry.properties:
                    diff_lua.append(f"['{entry.symbol()}'] = {{")
                    diff_lua.append(f"label = '{entry.properties.get('label')}',")
                    if "icon" in entry.properties:
                        diff_lua.append(f"icon = '{entry.properties['icon']}',")
                    diff_lua.append("},")
                else:
                    diff_lua.append(f"['{entry.symbol()}'] = {{}},")
            else:
                diff_lua.append(f"['{entry.symbol()}'] = {{}},")
        diff_lua.append("},")
        if len(diff["delete"]) == 0:
            diff_lua.append("delete = {},")
        else:
            diff_lua.append("delete = {")
            for entry in diff["delete"]:
                if isinstance(entry, Object):
                    diff_lua.append(f"['{entry.symbol()}'] = {{}},")
                else:
                    diff_lua.append(f"['{entry.symbol()}'] = {{}},")
            diff_lua.append("},")
        diff_lua.append("},")
        res += diff_lua
        counter += 1
    res.append("}")
    return "\n".join(res)
