import json

from constants.constants import get_path

default_locale = "en_us"
cached_strings = {}


def refresh():
    global cached_strings
    file = get_path("constants", f"{default_locale}.json")
    with open(file) as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
