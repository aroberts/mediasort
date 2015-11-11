import logging
logger = logging.getLogger(__name__)

import os
import shutil

import click

from fuzzywuzzy import process

from mediasort.act import Action
from mediasort.lib import as_list
from mediasort.lib import validate


class CopyTo(Action):
    __key__ = "copy_to"

    def validate_options(self):
        self.dir_must_exist(self.destination(), 'destination')

    def destination(self):
        return self.options.get('destination')

    def perform(self, dry_run):
        path = self.options['target'].path

        logger.info("copying '%s' to '%s'" % (path, self.destination()))
        if os.path.isfile(path):
            action = self.copy_file
        elif os.path.isdir(path):
            action = self.copy_dir
        else:
            raise click.ClickException("Couldn't find path: %s" % path)

        if not dry_run:
            action(path, self.destination())


    def copy_file(self, src, dst_root):
        shutil.copy(src, dst_root)

    def copy_dir(self, src, dst_root):
        shutil.copytree(src, os.path.join(dst_root, os.path.basename(src)))


class CopyToSubdir(CopyTo):
    __key__ = 'copy_to_subdir'

    def validate_options(self):
        self.dir_must_exist(self.options.get('destination'), 'destination')
        self.validate_subdir()
        self.ensure_destination_exists()

    def ensure_destination_exists(self):
        path = self.destination()
        if not os.path.exists(path):
            os.makedirs(path)

    def validate_subdir(self):
        if 'subdir' not in self.options:
            raise click.ClickException("copy_to_subdir needs a subdir")

    def subdir():
        return self.options.get('subdir')

    def destination(self):
        return os.path.join(
            self.options.get('destination'),
            self.subdir(),
        )

class CopyToMatchingSubdir(CopyToSubdir):
    __key__ = 'copy_to_matching_subdir'

    def validate_subdir(self):
        if 'subdir' in self.options:
            raise click.ClickException(
                "can't pass a subdir to copy_to_matching_subdir"
            )

    def subdir(self):
        if 'chosen_subdir' not in self.options:
            self.choose_subdir()
        return self.options['chosen_subdir']

    def choose_subdir(self):
        root = self.options.get('destination')
        haystack = [d for d in os.listdir(root)
                    if os.path.isdir(os.path.join(root, d))]

        name = os.path.basename(self.options['target'].path)
        choice = process.extractOne(name, haystack)

        if choice[1] >= self.options.get('score_cutoff', 90):
            self.options['chosen_subdir'] = choice[0]
        else:
            self.options['chosen_subdir'] = self.options['target'].name


class CopyContentsTo(CopyTo):
    __key__ = 'copy_contents_to'

    def perform(self, path, dry_run):
        contents = [os.path.join(path, f) for f in os.listdir(path)]
        only = as_list(self.options.get('only', []))
        exclude = as_list(self.options.get('exclude', []))

        for f in contents:
            ext = os.path.splitext(f)[1]
            if ((only and ext in only) or
              (not only and exclude and ext not in exclude) or
              (not only and not exclude)):
                super(CopyContentsTo, self).perform(f, dry_run=dry_run)

            else:
                logger.info("%s did not pass extension filter" % f)

