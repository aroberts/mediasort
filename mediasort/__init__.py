import logging
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


from mediasort.lib import enum
MEDIA_TYPES = enum(
    'tv',
    'movie',
    'music',
    'lossless_music',
    'other'
)

