from collections import namedtuple
def enum(*keys, **kw):
    return namedtuple('Enum', keys)(*keys)

def as_list(obj, types=(list)):
    if not isinstance(obj, types):
        obj = [obj]
    return obj

