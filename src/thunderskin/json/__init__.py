# MIT License

# Copyright (c) 2026 SOgz12Z3Ce

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""JSON package.

This package exposes some functions to load JSON files as `Object`s.

functions beginning with "load" return one or more `Object`s. But `load_core` returns `L10nObject`s.

Attributes:
    DeserializeAction: A enum class to control fixing game origin JSON files behaviour.
    deserialize: Deserialize a JSON file and try to fix it.
    load_data: Load `Object` from JSON deserialization data.
    load_file: Load `Object`s from a JSON file.
    load_dir: Load `Object`s from all JSON files in a directory.
    load_core: Load `L10nObject`s from original game JSON files. `directory` is the content.
    directory.

"""

import hashlib
import json
import re
import warnings
from enum import StrEnum
from pathlib import Path

from thunderskin.exceptions import ConflictObjectsError, UnreachableError
from thunderskin.json.patterns import FILEHASH_PATTERN_DICT, PATTERN_REPLACEMENT_DICT
from thunderskin.json.types import JsonValue
from thunderskin.l10n import L10nObject
from thunderskin.object import Object


class DeserializeAction(StrEnum):
    """A enum class to control `deserialize` fixing action."""

    IMPLICITLY_FIX = "implicitly_fix"  # Default. Fix json files and send info message.
    FIX = "fix"  # Fix json files if can.
    DONTFIX = "dont_fix"  # Don't fix json files.


def deserialize(
    file: Path,
    action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
) -> dict[str, JsonValue]:
    """Deserialize a json file and try to fix errors."""
    try:
        data = json.loads(Path(file).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as err:
        if action == DeserializeAction.DONTFIX:
            raise
        if action in {DeserializeAction.IMPLICITLY_FIX, DeserializeAction.FIX}:
            file_hash = hashlib.sha256(file.read_bytes()).hexdigest()
            if file_hash not in FILEHASH_PATTERN_DICT:
                raise
            content = file.read_text(encoding="utf-8-sig")
            for pattern in FILEHASH_PATTERN_DICT[file_hash]:
                content = content.replace(pattern, PATTERN_REPLACEMENT_DICT[pattern])
            data = json.loads(content)
        else:
            raise UnreachableError from err
        if action == DeserializeAction.IMPLICITLY_FIX:
            warnings.warn(
                f'"{file}" is from original CS and it is not a standard json file. '
                "The error part has been fixed implicitly. Call with "
                '"action=thunderskin.DeserializeAction.DONT_FIX" to stop fixing. Call '
                'with "action=thunderskin.DeserializeAction.FIX" to suppress info '
                "message.",
                UserWarning,
                stacklevel=2,
            )
    return data


def load_data(data: dict[str, JsonValue], l10n: str) -> list[Object]:
    """Load `Object`s from JSON data."""
    group = next(iter(data))
    return [Object(group, l10n, properties) for properties in data[group]]


def load_file(
    file: Path,
    action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
    l10n: str | None = None,
) -> list[Object]:
    """Load a JSON file."""
    data = deserialize(file, action)
    if l10n is not None:
        return load_data(data, l10n)

    path_str = file.as_posix()
    l10ns = re.findall("loc_(.*?)/", path_str)
    if len(l10ns) == 1:
        l10n = l10ns[0]
        warnings.warn(
            f'"{file}" is inferred to be a localization file for {l10n}. Call with '
            '"l10n=<language code>" to fix or supress this warning.',
            UserWarning,
            stacklevel=2,
        )
    else:
        l10n = "en"
        warnings.warn(
            f'Unable to infer if "{file}" is a localization file or not. Assume it is '
            'not a localization file ("en"). Call with "l10n=<language code>" to fix '
            "or supress this warning.",
            UserWarning,
            stacklevel=2,
        )
    return load_data(data, l10n)


def load_dir(
    directory: Path,
    action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
    l10n: str | None = None,
) -> list[Object]:
    """Load all JSON files from a directory."""
    objects = []
    files = [p for p in directory.rglob("*.json") if p.is_file()]
    for file in files:
        objects += load_file(file, action, l10n)
    return objects


def load_core(directory: Path) -> list[Object]:
    """Load original game JSON files."""
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
        cur_objects = load_dir(subdir, DeserializeAction.FIX, l10n)
        objects += deduplicate(cur_objects)
    return objects


def load_mod(directory: Path) -> list[Object]:
    objects = []
    content = directory / "content"
    objects += load_dir(content, DeserializeAction.DONTFIX, "en")
    loc = directory / "loc"
    if not loc.exists():
        return objects
    for subdir in [p for p in loc.iterdir() if p.is_dir()]:
        name = subdir.name()
        if not name.startswith("loc_"):
            continue
        l10n = name[4:]
        objects += load_dir(subdir, DeserializeAction.DONTFIX, l10n)
    return objects


def deduplicate(objects: list[Object]) -> list[Object]:
    symbol_object_map = {}
    for obj in objects:
        symbol = obj.symbol()
        if symbol in symbol_object_map:
            if symbol_object_map[symbol] != obj:
                raise ConflictObjectsError
            continue
        symbol_object_map[symbol] = obj
    return [obj for obj in symbol_object_map.values()]
