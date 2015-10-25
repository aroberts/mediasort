import re

from mediasort.classify.omdb import Omdb
from mediasort.classify.classification import Classification, MEDIA_TYPES

from mediasort.classify.tv import SEASON_NAME_REGEX

import logging
logger = logging.getLogger(__name__)

TITLE_AND_YEAR_REGEX = re.compile(r'^(.*)[.-_ ](\d{4})')
HD_YEAR_RES_REGEX = re.compile(
    r'^(.*)[.-_ ](\d{4})[.-_ ]((?:480|720|1080)(?:p|i))',
    re.IGNORECASE
)

omdb = Omdb()

def detect_movie(f):
    score = 0

    if SEASON_NAME_REGEX.search(f):
        return Classification.none()

    hd_match = HD_YEAR_RES_REGEX.search(f)
    title_match = TITLE_AND_YEAR_REGEX.search(f)

    if hd_match:
        resolution = hd_match.group(3)
        parts = re.split('[-_. ]', hd_match.group(1))
        title = ' '.join(filter(None, parts))
        year = hd_match.group(2)
        score = 6

    elif title_match:
        parts = re.split('[-_. ]', title_match.group(1))
        title = ' '.join(filter(None, parts))
        year = title_match.group(2)
        score = 4
    else:
        return Classification.none()

    logger.debug(title)
    logger.debug(year)

    rv = omdb.api(title=title, year=year)
    if rv:
        logger.debug('Response: %s' % rv.get("Response"))
        logger.debug('Type: %s' % rv.get("Type"))
        if rv.get("Response") == "True" and rv.get("Type") == "movie":
            return Classification(MEDIA_TYPES.movie, score)

    return Classification.none()
