import os

from mediasort.act import Action

class CopyTo(Action):
    __key__ = "copy_to"

    def validate_options(self):
        if 'destination' not in self.options:
            raise Exception("copy_to needs a destination")

        if not os.path.isdir(self.options['destination']):
            raise Exception("copy_to's destination must be a directory that exists")

    def perform(path):
        print "copying '%s' to '%s'" % (path, self.options.destination)


