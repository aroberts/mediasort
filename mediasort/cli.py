from mediasort import setup_logging

from mediasort.classify import Classifier
from mediasort.classify.classification import Classification

from mediasort.act import Action

import logging
logger = logging.getLogger(__name__)

import click
import yaml

config_option = click.option('--config', '-c',
                             type=click.File(),
                             help='path to config.yml')
dry_run_option = click.option('--dry-run', '-d',
                              help='don\'t make any filesystem changes',
                              is_flag=True,
                              default=False)
path_option = click.argument('path')


@click.command()
@config_option
@dry_run_option
@path_option
def classify(config, dry_run, path):
    if not config:
        raise Exception("Need config")

    conf = yaml.load(config)
    setup_logging(conf)
    classifier = Classifier(conf)
    rv = classifier.classify(path)
    for action_set in classifier.actions_for(rv):
        for action in Action.from_config(action_set):
            action.perform(path, dry_run=dry_run)
