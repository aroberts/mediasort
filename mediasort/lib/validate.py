import click
import os

class Validatable(object):
    def dir_must_exist(self, path, key):
        msg = "%s requires '%s' to be a directory that exists (%s)" % (
            self.__key__, key, path
        )

        if path == None or not os.path.isdir(path):
            raise click.ClickException(msg)

