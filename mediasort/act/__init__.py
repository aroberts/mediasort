import logging
logger = logging.getLogger(__name__)

import click

from mediasort.lib.validate import Validatable

registry = {}

NO_KEY = object()

class ActionMetaclass(type):
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        key = attrs.get('__key__', NO_KEY)
        if key == NO_KEY:
            raise Exception("Need to supply __key__ with Action declaration")

        if key in registry:
            raise Exception("'%s' already taken: '%s'" % (key, registry[key]))

        registry[key] = cls
        return cls

class Action(Validatable):
    __metaclass__ = ActionMetaclass
    __key__ = None

    def __init__(self, options):
        self.options = options

    @classmethod
    def from_config(cls, action_hash, classification):

        definitions = action_hash['perform']
        if isinstance(definitions, dict):
            definitions = [definitions]

        try:
            actions = [
                registry[action](options)
                for d in definitions
                for action, options in d.items()
            ]

            for action in actions:
                action.options['target'] = classification
                action.validate_options()

            return actions
        except KeyError, e:
            msg = "Available actions: %s" % registry.keys()
            logger.error(e.message)
            logger.error(msg)
            raise click.ClickException(msg)

    def perform(**kwargs):
        raise NotImplementedError()

    def validate_options(self):
        pass


from mediasort.act.copy_to import CopyTo
from mediasort.act.copy_to import CopyContentsTo
