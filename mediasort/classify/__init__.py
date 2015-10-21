import operator
import os

from mediasort.classify.omdb import Omdb
from mediasort.classify.imdb import (
    find_nfos,
    extract_imdb_id,
)

from mediasort.classify.tv import detect_tv
from mediasort.classify.movies import detect_movie

from mediasort import MEDIA_TYPES

import logging
logger = logging.getLogger(__name__)

class Classifier(object):

    def __init__(self, root_path):
        self.root_path = root_path
        self.omdb = Omdb()


    def classify(self, path):
        full_path = os.path.join(self.root_path, path)

        # Try to classify by NFO
        by_nfo = self.classify_by_nfo(full_path)
        if by_nfo:
            logger.debug("[NFO] %s" % path)
            return by_nfo

        # next, detect via tv module
        if detect_tv(path):
            return MEDIA_TYPES.tv

        # next, detect via movie module
        if detect_movie(path):
            return MEDIA_TYPES.movie

        return MEDIA_TYPES.other


    def classify_by_nfo(self, full_path):

        if os.path.isdir(full_path):
            nfos = find_nfos(full_path)
            ids = [extract_imdb_id(nfo) for nfo in nfos]
            omdb_responses = filter(None, [self.omdb.api(imdb=i) for i in ids])
            omdb_types = map(operator.itemgetter('Type'), omdb_responses)

            if 'movie' in omdb_types:
                return MEDIA_TYPES.movie

            elif set(['episode', 'series']).intersection(omdb_types):
                return MEDIA_TYPES.tv

        return None
