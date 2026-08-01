from thunderskin.l10n.localizers import (
    localize_str,
    localize_str_dict,
    localize_slots,
    localize_deck,
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
        "startlabel": localize_str,
        "label": localize_str,
        "slot": localize_slot,
        "slots": localize_slots,
    },
}
