import hashlib
import json
import re
from enum import StrEnum
from pathlib import Path

from thunderskin.json.patterns import FILEHASH_PATTERN_DICT, PATTERN_REPLACEMENT_DICT
from thunderskin.exceptions import UnreachableError
from thunderskin.object import Object
from thunderskin.json.types import JsonValue


class DeserializeAction(StrEnum):
    IMPLICITLY_FIX = "implicitly_fix"  # Default. Fix json files and send info message.
    FIX = "fix"  # Fix json files if can.
    DONTFIX = "dont_fix"  # Don't fix json files.


def deserialize(
    file: Path, action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX
) -> dict[str, JsonValue]:
    """Deserialize a json file and try to fix errors."""
    try:
        data = json.loads(Path(file).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        if action == DeserializeAction.DONTFIX:
            # print(file)
            raise
        if (
            action == DeserializeAction.IMPLICITLY_FIX
            or action == DeserializeAction.FIX
        ):
            file_hash = hashlib.sha256(file.read_bytes()).hexdigest()
            if file_hash not in FILEHASH_PATTERN_DICT:
                raise
            content = file.read_text(encoding="utf-8-sig")
            for pattern in FILEHASH_PATTERN_DICT[file_hash]:
                content = content.replace(pattern, PATTERN_REPLACEMENT_DICT[pattern])
            data = json.loads(content)
        else:
            raise UnreachableError
        if action == DeserializeAction.IMPLICITLY_FIX:
            print(
                f'[INFO] "{file}" is from original CS and it is not a standard json file. The error part has been fixed implicitly. Call with "action=thunderskin.DeserializeAction.DONT_FIX" to stop fixing. Call with "action=thunderskin.DeserializeAction.FIX" to suppress info message.'
            )
    return data


def load_data(data: dict[str, JsonValue], l10n: str) -> list[Object]:
    objects = []
    group = next(iter(data))
    for properties in data[group]:
        objects.append(Object(group, l10n, properties))
    return objects


def load_file(
    file: Path,
    action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
    l10n: str | None = None,
) -> list[Object]:
    data = deserialize(file, action)
    if l10n is not None:
        return load_data(data, l10n)

    path_str = file.as_posix()
    l10ns = re.findall("loc_(.*?)/", path_str)
    if len(l10ns) == 1:
        l10n = l10ns[0]
        print(
            f'[WARN] "{file}" is inferred to be a localization file for {l10n}. Call with l10n=<language code> to fix or supress this warning.'
        )
    else:
        l10n = "en"
        print(
            f'[WARN] Unable to infer if "{file}" is a localization file or not. Assume it is not a localization file ("en"). Call with l10n=<language code> to fix or supress this warning.'
        )
    return load_data(data, l10n)


def load_dir(
    directory: Path,
    action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
    l10n: str | None = None,
) -> list[Object]:
    objects = []
    files = [p for p in directory.rglob("*.json") if p.is_file()]
    for file in files:
        objects += load_file(file, action, l10n)
    return objects


def load_core(directory: Path) -> list[Object]:
    objects = []
    for subdir in [p for p in directory.iterdir() if p.is_dir()]:
        l10n = ""
        match subdir.name:
            case "core":
                l10n = "en"
            case "loc_de":
                l10n = "de"
            case "loc_es":
                l10n = "es"
            case "loc_fr":
                l10n = "fr"
            case "loc_jp":
                l10n = "jp"
            case "loc_ru":
                l10n = "ru"
            case "loc_zh-hans":
                l10n = "zh-hans"
        objects += load_dir(subdir, DeserializeAction.FIX, l10n)
    return objects


# def load_mod(directory: Path) -> list[Object]:
#     objects = []
#     for subdir in [p for p in directory.iterdir() if p.is_dir()]:
#         match subdir.name:
#             case "content":
#                 objects += load_dir(subdir, DeserializeAction.DONTFIX, "en")
#             case "loc":
#                 for locdir in [p for p in subdir.iterdir() if p.is_dir()]:
#                     match = re.search("loc_(.*)", locdir.as_posix())
#                     if match is None:
#                         continue
#                     l10n = match.group(0)
#                     objects += load_dir(locdir, DeserializeAction.DONTFIX, l10n)
#     return objects
