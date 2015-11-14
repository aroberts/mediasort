import logging
logger = logging.getLogger(__name__)

import click

from mediasort.lib.validate import Validatable
from mediasort.lib import as_list
from mediasort.classify.classification import MEDIA_TYPES

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
    def validate_definition(cls, definition):
        errors = []
        if 'media_type' not in definition:
            errors.append("is missing `media_type`")
        if definition['media_type'] not in MEDIA_TYPES:
            errors.append("has an invalid `media_type`")

        if 'confidence' not in definition:
            errors.append("is missing `confidence`")
        if not isinstance(definition['confidence'], (int, float)):
            errors.append("must provide `confidence` as a number")

        if 'perform' not in definition:
            errors.append("is missing `perform`")

        for perform in as_list(definition['perform']):
            for key, options in perform.items():
                options['target'] = None

                if key in registry:
                    action = registry[key](options)
                    try:
                        action.validate_options()
                    except click.ClickException, e:
                        errors.append("error: %s" % e.message)
                else:
                    errors.append("references unknown perform: '%s'" % key)

        return errors

    def error_message(self, msg):
        return "%s: %s" % (self.__key__, msg)


    @classmethod
    def from_config(cls, action_hash, classification):

        try:
            actions = [
                registry[action](options)
                for d in as_list(action_hash['perform'])
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


from mediasort.act import copy_to
from mediasort.act import plex
