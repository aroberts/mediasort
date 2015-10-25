import sys
import os

from mediasort.classify import Classifier

import logging
logger = logging.getLogger(__name__)

from collections import defaultdict

import click

config_option = click.option('--config', '-c', help='path to config.yml')
path_option = click.argument('path')


@click.command()
@config_option
@path_option
def classify(config, path):
    if not config:
        raise Exception("Need config")

    classifier = Classifier('/')
    print classifier.classify(path)




root = "/Volumes/Download"

def main():
    categories = defaultdict(list)

    classifier = Classifier(root)

    for f in os.listdir(root):
        c = classifier.classify(f)
        categories[c.media_type].append((f, c.score))

    for label, entries in categories.items():
        print label
        print "---------------------"
        for m in entries:
            print m
        print ""

if __name__ == "__main__":
    main()
