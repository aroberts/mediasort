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

class Action(object):
    __metaclass__ = ActionMetaclass
    __key__ = None

    def __init__(self, options):
        self.options = options

    @classmethod
    def from_config(cls, action_hash):
        actions = [
            registry[action](options)
            for action, options in action_hash['perform'].items()
        ]
        [a.validate_options() for a in actions]
        return actions

    def perform(path):
        raise NotImplementedError()

    def validate_options(self):
        pass

