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

    def __init__(self, root_path):
        self.root_path = root_path
        self.omdb = Omdb()

    def get_types(self, path):
        types = []
        full_path = os.path.join(self.root_path, path)
        if os.path.isdir(full_path):
            for folder, _, files in os.walk(full_path):
                for filename in files:
                    types.append(mimetypes.guess_type(filename)[0])

        else:
            types.append(mimetypes.guess_type(path)[0])

        return filter(None, list(set(types)))

    def classify(self, path):
        full_path = os.path.join(self.root_path, path)

        types = self.get_types(path)

        classifications = [
            self.classify_by_nfo(full_path),
            Classification.none(),
        ]

        if any(['video' in t for t in types]):
            classifications.extend([
                detect_tv(path),
                detect_movie(path),
            ])

        return max(classifications)


    def classify_by_nfo(self, full_path):

        if os.path.isdir(full_path):
            nfos = find_nfos(full_path)
            ids = [extract_imdb_id(nfo) for nfo in nfos]
            omdb_responses = filter(None, [self.omdb.api(imdb=i) for i in ids])
            omdb_types = map(operator.itemgetter('Type'), omdb_responses)

            if 'movie' in omdb_types:
                return Classification(MEDIA_TYPES.movie, 10)

            elif set(['episode', 'series']).intersection(omdb_types):
                return Classification(MEDIA_TYPES.tv, 10)

        return None
