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

"""Game object package.

This package exposes `Object` for managing files deserialization.
"""

from thunderskin.json.types import JsonObject
from thunderskin.object.escape import escape


class Object:
    """A game object.

    All `JsonObject` from `GameJson` are considered as `Object`s, no matter they are
    from core or localization folder.
    """

    def __init__(self, group: str, l10n: str, properties: JsonObject) -> None:
        """Initialize `Object`.

        Args:
            group: Object type (the root key). It can be:
                - achievements
                - cultures
                - decks
                - dicta
                - elements
                - endings
                - legacies
                - levers
                - portals
                - recipes
                - settings
                - verbs
            l10n: Localization string. "en" is for the original game.
            properties: Object properties.

        """
        self.group = group
        self.l10n = l10n
        self.properties = properties

    def __eq__(self, other):
        if not isinstance(other, Object):
            return NotImplemented
        return (
            self.group == other.group
            and self.l10n == other.l10n
            and self.properties == other.properties
        )

    def id(self):
        return self.properties["id"]

    def unique_id(self):
        return f"{self.group}/{self.id()}"

    def key(self):
        return escape(self.unique_id())
