import logging
logger = logging.getLogger(__name__)

import os
import shutil

import click

from mediasort.act import Action
from mediasort.lib import as_list
from mediasort.lib import validate


class UpdatePlexSection(Action):
    '''
    update_plex_section:
        server_address: http://...
        section_name: ...
    '''

    __key__ = "update_plex_section"



