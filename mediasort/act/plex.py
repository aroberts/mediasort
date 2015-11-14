import logging
logger = logging.getLogger(__name__)

import os
from xml.etree import ElementTree as ET
import requests

import click

from mediasort.act import Action
from mediasort.lib import as_list
from mediasort.lib import validate


class RefreshPlexSection(Action):
    '''
    refresh_plex_section:
        server_address: http://...
        section_name: ...
    '''

    __key__ = "refresh_plex_section"

    def validate_options(self):
        if 'section_name' not in self.options:
            raise click.ClickException('refresh_plex_section needs section_name')
        if 'server_address' not in self.options:
            raise click.ClickException('refresh_plex_section needs server_address')

    def perform(self, dry_run):
        section_path = 'library/sections'
        sections = ET.fromstring(self._plex_request(section_path))
        xpath = './/Directory[@title="%s"]' % self.options['section_name']
        section = sections.find(xpath)

        if not section:
            msg = "Couldn't find section '%s'" % self.options['section_name']
            raise click.ClickException(self.error_message(msg))

        if not dry_run:
            return self._plex_request(
                '/'.join([section_path, section.attrib['key'], 'refresh'])
            )


    def _plex_request(path, method='get', **data):
        request = getattr(requests, method.lower())
        url = '/'.join([self.options['server_address'], path])
        response = request(url, **data)

        try:
            response.raise_for_status()
        except e:
            raise click.ClickException(e.message)


        return response.content




