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

"""JSON types module.

This module provides some types to represent JSON types.

Examples:
    def deserialize(
        file: Path, action: DeserializeAction = DeserializeAction.IMPLICITLY_FIX,
    ) -> GameJson

Attributes:
    JsonPrimitive: JSON basic values.
    JsonObject: JSON object.
    JsonArray: JSON array.
    JsonValue: Types can be JSON value.
    JsonProperty: JSON key-value pair.
    JsonToken: Any JSON Node.
    GameJson: Valid game JSON file.

"""

type JsonPrimitive = str | int | float | bool | None
type JsonObject = dict[str, JsonValue]
type JsonArray = list[JsonValue]
type JsonValue = JsonPrimitive | JsonObject | JsonArray
type JsonProperty = tuple[str, JsonValue]
type JsonToken = JsonObject | JsonArray | JsonProperty | JsonPrimitive

type GameJson = dict[str, JsonArray]
