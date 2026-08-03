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

"""Localization registry module.

This module provides `L10N_REGISTRY` for localizing a core `Object` with a localization
`Object`. The first layer shows which part of registry should `Object`s in different
groups use. The further layers recursively shows which part of registry should
different properties should use. Once reaching a function, call it with core
properties and localization properties can finish localization. These localizers always
modify core properties (if can) but also return localized properties so you can just
assign it.

Example:
    See `thunderskin.l10n.localize`.

Attributes:
    L10N_REGISTRY: The localization registry.

"""

from thunderskin.l10n.localizers import (
    localize_deck,
    localize_slot,
    localize_slots,
    localize_str,
    localize_str_dict,
)

L10N_REGISTRY = {
    "achievements": {
        "label": localize_str,
        "descriptionlocked": localize_str,
        "descriptionunlocked": localize_str,
        "unlockmessage": localize_str,
    },
    "decks": localize_deck,
    "elements": {
        "label": localize_str,
        "description": localize_str,
        "slots": localize_slots,
        "xexts": localize_str_dict,
    },
    "endings": {
        "label": localize_str,
        "description": localize_str,
    },
    "legacies": {
        "label": localize_str,
        "description": localize_str,
        "startdescription": localize_str,
    },
    "portals": {
        "label": localize_str,
        "description": localize_str,
        "icon": localize_str,
    },
    "recipes": {
        "startlabel": localize_str,
        "label": localize_str,
        "startdescription": localize_str,
        "description": localize_str,
        "slots": localize_slots,
        "internaldeck": localize_deck,
    },
    "verbs": {
        "label": localize_str,
        "description": localize_str,
        "slot": localize_slot,
        "slots": localize_slots,
    },
}
