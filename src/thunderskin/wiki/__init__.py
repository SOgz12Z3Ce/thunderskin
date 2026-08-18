from thunderskin.object import Object
from thunderskin.package import Package
from thunderskin.resource import Resource
from thunderskin.wiki.escape import escape
from thunderskin.json.types import JsonObject


def title(package: Package, entry: Object) -> str:
    return escape(f"{package.name}/{package.version}/{entry.symbol()}")


def diff_list_to_lua(
    diff_list: list[dict[str, list[Object | Resource]]], versions: list[str], dependencies: list[list[tuple[str, str]]], name: str
) -> str:
    res = ["local p = {"]
    res.append(f"name = '{name}',")
    res.append("diff = {")
    counter = 0
    reversed_versions = list(reversed(versions))
    reversed_dependencies = list(reversed(dependencies))
    for diff in reversed(diff_list):
        diff_lua = ["{"]
        diff_lua.append(f"version = '{reversed_versions[counter]}',")
        cur_deps = reversed_dependencies[counter]
        if len(cur_deps) == 0:
            diff_lua.append("dependency = {},")
        else:
            diff_lua.append("dependency = {")
            for dep in cur_deps:
                diff_lua.append(f"['{dep[0]}'] = '{dep[1]}',")
            diff_lua.append("},")
        diff_lua.append("new = {")
        for entry in diff["new"]:
            if isinstance(entry, Object):
                kvps = []
                if "icon" in entry.properties:
                    kvp = ("icon", f"'{entry.properties['icon']}'")
                    kvps.append(kvp)
                if "label" in entry.properties:
                    kvp = (
                        "label",
                        f'\'{entry.properties.get('label').replace("'", "\\'")}\'',
                    )
                    kvps.append(kvp)
                if "isAspect" in entry.properties:
                    is_aspect = entry.properties["isAspect"]
                    if is_aspect is True:
                        kvp = ("isAspect", "true")
                        kvps.append(kvp)
                if len(kvps) > 0:
                    diff_lua.append(f"['{entry.symbol()}'] = {{")
                    for kvp in kvps:
                        diff_lua.append(f"{kvp[0]} = {kvp[1]},")
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
    res.append("},")
    res.append("}")
    res.append("")
    res.append("return p")
    return "\n".join(res)
