import os
import re

from mediasort.classify.classification import Classification, MEDIA_TYPES


SEASON_NAME_REGEX = re.compile(r'(.*)(S\d\d?E\d\d?)', re.IGNORECASE)
WHOLE_SEASON_REGEX = re.compile(r'(.*)(Season.?\d+)', re.IGNORECASE)

def detect_tv(path):
    f = os.path.basename(path)

    match = SEASON_NAME_REGEX.search(f)
    if match:
        return Classification(path, MEDIA_TYPES.tv, 6, name=match.group(1))

    match = WHOLE_SEASON_REGEX.search(f)
    if match:
        return Classification(path, MEDIA_TYPES.tv, 4, name=match.group(1))

    return Classification.none(path)

