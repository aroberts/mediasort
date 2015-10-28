from mediasort import setup_logging

from mediasort.classify import Classifier
from mediasort.classify.classification import Classification

from mediasort.act import Action

import logging
logger = logging.getLogger(__name__)

import click
import yaml

config_option = click.option('--config', '-c', help='path to config.yml')
path_option = click.argument('path')


@click.command()
@config_option
@path_option
def classify(config, path):
    if not config:
        raise Exception("Need config")

    conf = load_config(config)
    setup_logging(conf)
    classifier = Classifier(conf)
    rv = classifier.classify(path)
    for action_set in classifier.actions_for(rv):
        for action in Action.from_config(action_set):
            action.perform(path)

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.load(f)
