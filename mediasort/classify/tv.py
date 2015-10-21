import re

SEASON_NAME_REGEX = re.compile(r'(S\d\d?E\d\d?)', re.IGNORECASE)
WHOLE_SEASON_REGEX = re.compile(r'(Season.?\d+)', re.IGNORECASE)

def detect_tv(f):
    return has_season_in_name(f)


def has_season_in_name(path):
    return (SEASON_NAME_REGEX.search(path) or
            WHOLE_SEASON_REGEX.search(path))

