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

"""Localizers module.

This module provides localizers. Localizers are functions accepting core properties and
localization properties, returning localized properties. Localizers accept and return
same type of parameters and always modify `target` parameter (if can).

Examples:
    Usage of `localize_str_dict`:

        from thunderskin.l10n.localizers import localize_str_dict

        target = {
            "demo_id_1": "demo string 1",
            "demo_id_2": "demo string 2",
        }
        reference = {
            "demo_id_1": "演示字符串 1",
            "demo_id_2": "演示字符串 2",
        }
        target = localize_str_dict(target, reference)

Attributes:
    localize_str: For general string.
    localize_str_dict: For dict[str, str].
    localize_deck: For `Deck`.
    localize_slots: For `Slot` list.
    localize_slot: For `Slot`.

"""

from thunderskin.json.types import JsonObject


def localize_str(_target: str, reference: str) -> str:
    """Localize a `str`."""
    return reference


def localize_str_dict(
    target: dict[str, str],
    reference: dict[str, str],
) -> dict[str, str]:
    """Localize a `dict[str, str]` (`drawmessages` and `xexts` properties)."""
    for key in target:
        if key not in reference:
            continue
        target[key] = reference[key]
    return target


def localize_deck(target: JsonObject, reference: JsonObject) -> JsonObject:
    """Localize a slot list (`internaldeck` property or a `decks` group `Object`)."""
    if "label" in target and "label" in reference:
        target["label"] = localize_str(target["label"], reference["label"])
    if "description" in target and "description" in reference:
        target["description"] = localize_str(
            target["description"],
            reference["description"],
        )
    if "drawmessages" in target and "drawmessages" in reference:
        target["drawmessages"] = localize_str_dict(
            target["drawmessages"],
            reference["drawmessages"],
        )
    return target


def localize_slots(
    target: list[JsonObject],
    reference: list[JsonObject],
) -> list[JsonObject]:
    """Localize a slot list (`slots` property)."""
    target_id_slot_map = {slot["id"]: slot for slot in target}
    reference_id_slot_map = {slot["id"]: slot for slot in reference}
    res = []
    for key, value in target_id_slot_map:
        if key not in reference_id_slot_map:
            continue
        target_slot = target_id_slot_map[key]
        reference_slot = value
        res.append(localize_slot(target_slot, reference_slot))
    return res


def localize_slot(target: JsonObject, reference: JsonObject) -> JsonObject:
    """Localize a slot (`slot` property or member of `slots` property)."""
    if "label" in target and "label" in reference:
        target["label"] = reference["label"]
    if "description" in target and "description" in reference:
        target["description"] = reference["description"]
    return target
