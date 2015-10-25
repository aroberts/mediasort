from mediasort.lib import enum
MEDIA_TYPES = enum(
    'tv',
    'movie',
    'music',
    'lossless_music',
    'other'
)

class Classification(object):
    def __init__(self, mtype, score):
        self.media_type = mtype
        self.score = score

    @classmethod
    def none(cls):
        return cls(mtype=MEDIA_TYPES.other, score=0)

    def __eq__(self, other):
        try:
            return all([self.media_type == other.media_type,
                        self.score == other.score])
        except:
            return False

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return "%s(%s)" % (self.media_type, self.score)

    def __repr__(self):
        return str(self)

