import os

from mediasort.classify.classification import Classification, MEDIA_TYPES

def detect_music(path, types=None):
    count = len(types)
    if count > 100:
        return Classification.none(path)

    music_types = [t for t in types if 'audio' in t]
    score = int(round(float(len(music_types)) * 10 / count))

    mtype = None
    if any(['flac' in t for t in music_types]):
        mtype = MEDIA_TYPES.lossless_music
    else:
        mtype = MEDIA_TYPES.music

    if mtype:
        return Classification(path, mtype, score, name=os.path.basename(path))

    return Classification.none(path)

