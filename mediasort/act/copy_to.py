import logging
logger = logging.getLogger(__name__)

import os
import shutil

from mediasort.act import Action

class CopyTo(Action):
    __key__ = "copy_to"

    def validate_options(self):
        if 'destination' not in self.options:
            raise Exception("copy_to needs a destination")

        # if not os.path.isdir(self.options['destination']):
        #     raise Exception("copy_to's destination must be a directory that exists")


    def perform(self, path, dry_run):
        logger.info("copying '%s' to '%s'" % (path, self.options['destination']))
        if os.path.isfile(path):
            action = self.copy_file
        elif os.path.isdir(path):
            action = self.copy_dir
        else:
            raise Exception("Couldn't find path: %s" % path)

        if not dry_run:
            action(path, self.options['destination'])


    def copy_file(self, src, dst_root):
        shutil.copy(src, dst_root)

    def copy_dir(self, src, dst_root):
        shutil.copytree(src, os.path.join(dst_root, os.path.basename(src)))


