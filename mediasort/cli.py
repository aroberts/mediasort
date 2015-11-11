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

@click.group()
@config_option
@click.pass_context
def cli(ctx, config):
    conf = yaml.load(config)
    setup_logging(conf)

    ctx.obj = dict(
        config=conf
    )

@cli.command()
@path_option
def test(ctx, path):
    pass

@cli.command()
@path_option
def validate(ctx):
    pass

@cli.command()
@dry_run_option
@path_option
@click.pass_context
def classify(ctx, dry_run, path):
    config = ctx.obj['config']

    if not config:
        raise click.ClickException("You must provide a config")

    classifier = Classifier(config)

    if path.endswith('/'):
        path = path[:-1]

    rv = classifier.classify(path)

    logger.info("%s: %s" % (path, rv))

    for action_set in classifier.actions_for(rv):
        for action in Action.from_config(action_set, rv):
            action.perform(dry_run=dry_run)
