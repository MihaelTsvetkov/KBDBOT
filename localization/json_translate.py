import json
from options import settings


def get_json_localization(key):
    with open(settings.LANGUAGE, encoding='utf8') as phrase_file:
        result = json.load(phrase_file)[key]
    return result


def get_json_localization_buttons(key):
    with open(settings.LANGUAGE_BUTTONS, encoding='utf8') as phrase_file:
        result = json.load(phrase_file)[key]
    return result
