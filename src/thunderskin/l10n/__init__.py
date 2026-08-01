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

"""Localization object package.

This package exposes `L10nObject` for managing localization.
"""

from collections.abc import Callable

from thunderskin.json.types import JsonObject
from thunderskin.l10n.registry import L10N_REGISTRY
from thunderskin.object import Object


class L10nObject:
    """A localization object.

    `L10nObject` mantains a list of `Object`s and can merge localization texts into a
    `Object`.
    """

    def __init__(self, objects: list[Object]) -> None:
        """Initialize `L10nObject`.

        Args:
            objects: A list of `Object`s. At least one core `Object` required.
            All `Object`s must have same `id`.

        """
        self.group = objects[0].group
        self.l10n_properties_map = {}
        for obj in objects:
            self.l10n_properties_map[obj.l10n] = obj.properties

    def as_l10n(self, l10n: str) -> Object:
        """Get a localized `Object`."""
        core = self._core()
        l10n_obj = self.l10n_properties_map[l10n]

        return localize(
            core.properties.copy(),
            l10n_obj.properties,
            L10N_REGISTRY[core.group],
        )

    def _core(self) -> Object:
        return self.l10n_properties_map["en"]


def localize(
    target: JsonObject,
    reference: JsonObject,
    registry: dict[str, dict | Callable],
) -> JsonObject:
    """Localize properties recursively.

    Localize `target` with `reference`. The `registry` from thunderskin.l10n.registry
    can tell the localization way.
    """
    for key in target:
        if key not in registry:
            continue
        if callable(registry[key]):
            target[key] = registry[key](target[key], reference[key])
        else:
            target[key] = localize(target[key], reference[key], registry[key])
    return target
