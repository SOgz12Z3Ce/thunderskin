import hashlib
import json
from enum import StrEnum
from pathlib import Path

from thunderskin.types import JsonValue
from thunderskin.constants import FILEHASH_PATTERN_DICT, PATTERN_REPLACEMENT_DICT
from thunderskin.exceptions import UnreachableError
from thunderskin.object import Object


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
    except json.JSONDecodeError as e:
        if action == DeserializeAction.DONTFIX:
            raise e
        if (
            action == DeserializeAction.IMPLICITLY_FIX
            or action == DeserializeAction.FIX
        ):
            file_hash = hashlib.sha256(file.read_bytes()).hexdigest()
            if file_hash not in FILEHASH_PATTERN_DICT:
                raise e
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


def load_data(data: dict[str, JsonValue]) -> list[Object]:
    objects = []
    group = next(iter(data))
    for properties in data[group]:
        objects.append(Object(group, properties))
    return objects


def load_file(
    file: Path, action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX
) -> list[Object]:
    data = deserialize(file, action)
    return load_data(data)


def load_dir(
    directory: Path, action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX
) -> list[Object]:
    objects = []
    files = [p for p in directory.rglob("*.json") if p.is_file()]
    for file in files:
        objects += load_file(file, action)
    return objects
