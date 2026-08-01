from thunderskin.json.types import JsonValue


def localize_str(target: str, reference: str) -> str:
    return reference


def localize_str_dict(
    target: dict[str, str], reference: dict[str, str]
) -> dict[str, str]:
    for key in target.keys():
        if key not in reference:
            continue
        target[key] = reference[key]
    return target


def localize_deck(target: dict, reference: dict) -> dict:
    if "label" in target and "label" in reference:
        target["label"] = localize_str(target["label"], reference["label"])
    if "description" in target and "description" in reference:
        target["description"] = localize_str(
            target["description"], reference["description"]
        )
    if "drawmessages" in target and "drawmessages" in reference:
        target["drawmessages"] = localize_str_dict(
            target["drawmessages"], reference["drawmessages"]
        )
    return target


def localize_slots(
    target: List[JsonValue], reference: List[JsonValue]
) -> List[JsonValue]:
    target_id_slot_map = {slot["id"]: slot for slot in target}
    reference_id_slot_map = {slot["id"]: slot for slot in reference}
    res = []
    for key in target_id_slot_map.keys():
        target_slot = target_id_slot_map[key]
        if key not in reference_id_slot_map:
            continue
        res.append(localize_slot(target_slot, reference_slot))
    return res


def localize_slot(target: dict, reference: dict) -> dict:
    if "label" in target and "label" in reference:
        target["label"] = reference["label"]
    if "description" in target and "description" in reference:
        target["description"] = reference["description"]
    return target
