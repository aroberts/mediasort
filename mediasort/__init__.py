import logging
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s',
    "%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

import mimetypes

def setup_logging(config):
    if 'log_path' in config:
        handler = logging.FileHandler(config['log_path'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if 'log_level' in config:
        logger.setLevel(getattr(logging, config['log_level'].upper()))

def setup_mime(config):
    if 'mimetypes_path' in config:
        mimetypes.init([config['mimetypes_path']])
    if 'mimetypes_paths' in config:
        mimetypes.init(config['mimetypes_paths'])
