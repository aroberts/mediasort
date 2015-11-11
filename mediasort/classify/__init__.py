import operator
import os
import mimetypes

from mediasort.classify.omdb import Omdb
from mediasort.classify.imdb import (
    find_nfos,
    extract_imdb_id,
)

from mediasort.classify.tv import detect_tv
from mediasort.classify.movies import detect_movie

from mediasort.classify.classification import (
    MEDIA_TYPES,
    Classification,
)

import logging
logger = logging.getLogger(__name__)

class Classifier(object):

    def __init__(self, config):
        self.omdb = Omdb()
        self.config = config

    def get_types(self, path):
        types = []
        if os.path.isdir(path):
            for folder, _, files in os.walk(path):
                for filename in files:
                    types.append(mimetypes.guess_type(filename)[0])

        else:
            types.append(mimetypes.guess_type(path)[0])

        return filter(None, list(set(types)))

    def classify(self, path):
        types = self.get_types(path)

        classifications = [
            self.classify_by_nfo(path),
            Classification.none(path),
        ]

        if any(['video' in t for t in types]):
            classifications.extend([
                detect_tv(path),
                detect_movie(path),
            ])

        return max(classifications)

    def actions_for(self, classification):
        actions = self.config.get('actions', [])
        if not actions:
            logger.warn("No actions registered in config")
            return []

        return [a for a in actions
                if a['media_type'] == classification.media_type and
                a['confidence'] <= classification.score]


    def classify_by_nfo(self, path):

        if os.path.isdir(path):
            nfos = find_nfos(path)
            ids = [extract_imdb_id(nfo) for nfo in nfos]
            omdb_responses = filter(None, [self.omdb.api(imdb=i) for i in ids])
            omdb_types = map(operator.itemgetter('Type'), omdb_responses)

            if 'movie' in omdb_types:
                return Classification(path, MEDIA_TYPES.movie, 10)

            elif set(['episode', 'series']).intersection(omdb_types):
                return Classification(path, MEDIA_TYPES.tv, 10)

        return Classification.none(path)
