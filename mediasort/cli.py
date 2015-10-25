import sys
import os

from mediasort.classify import Classifier

import logging
logger = logging.getLogger(__name__)

from collections import defaultdict


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
