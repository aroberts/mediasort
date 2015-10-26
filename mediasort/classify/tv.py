import os
import re

SEASON_NAME_REGEX = re.compile(r'(S\d\d?E\d\d?)', re.IGNORECASE)
WHOLE_SEASON_REGEX = re.compile(r'(Season.?\d+)', re.IGNORECASE)

from mediasort.classify.classification import Classification, MEDIA_TYPES

def detect_tv(path):
    f = os.path.basename(path)

    if SEASON_NAME_REGEX.search(f):
        return Classification(MEDIA_TYPES.tv, 6)
    if WHOLE_SEASON_REGEX.search(f):
        return Classification(MEDIA_TYPES.tv, 4)
    return Classification.none()

