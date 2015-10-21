from collections import namedtuple
def enum(*keys, **kw):
    return namedtuple('Enum', keys)(*keys)


