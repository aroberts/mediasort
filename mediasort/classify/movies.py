import re

from mediasort.classify.omdb import Omdb

import logging
logger = logging.getLogger(__name__)

TITLE_AND_YEAR_REGEX = re.compile(r'^(.*) (\d{0,4})')
HD_YEAR_RES_REGEX = re.compile(
    r'^(.*)[.-_ ](\d{4})[.-_ ]((?:480|720|1080)(?:p|i))',
    re.IGNORECASE
)

omdb = Omdb()

def detect_movie(f):
    return detect_movie_with_res(f)

def detect_movie_with_res(f):
    match = HD_YEAR_RES_REGEX.search(f)
    if match:
        logger.debug(match.groups())
        resolution = match.group(2)
        parts = re.split('[-_. ]', match.group(1))
        title = ' '.join(filter(None, parts))
        year = match.group(2)

        logger.debug(title)
        logger.debug(year)

        rv = omdb.api(title=title, year=year)

        logger.debug('Response: %s' % rv.get("Response"))
        logger.debug('Type: %s' % rv.get("Type"))
        return rv.get("Response") == "True" and rv.get("Type") == "movie"

