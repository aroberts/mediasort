from mediasort.lib import enum
MEDIA_TYPES = enum(
    'tv',
    'movie',
    'music',
    'lossless_music',
    'other'
)

import re
SPACERS = re.compile(r'[ -._]')


class Classification(object):
    def __init__(self, path, mtype, score, name=None):
        self.path = path
        self.media_type = mtype
        self.score = score
        self.name = self.normalize_name(name)

    @classmethod
    def normalize_name(cls, name):
        if not name:
            return name
        return SPACERS.sub(' ', name).strip()

    @classmethod
    def none(cls, path):
        return cls(path=path, mtype=MEDIA_TYPES.other, score=0)

    def __eq__(self, other):
        try:
            return all([self.media_type == other.media_type,
                        self.score == other.score])
        except:
            return False

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        rv = "%s(%s)" % (self.media_type, self.score)
        if self.name:
            rv += " %s" % self.name
        return rv

    def __repr__(self):
        return str(self)

