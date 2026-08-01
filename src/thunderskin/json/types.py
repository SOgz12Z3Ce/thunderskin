type JsonPrimitive = str | int | float | bool | None
type JsonObject = dict[str, JsonValue]
type JsonArray = list[JsonValue]
type JsonValue = JsonPrimitive | JsonObject | JsonArray
type JsonProperty = tuple[str, JsonValue]
type JsonToken = JsonObject | JsonArray | JsonProperty | JsonPrimitive
