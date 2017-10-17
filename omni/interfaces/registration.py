from functools import partial
import itertools
from gym import error
import pkg_resources

def load(name):
    entry_point = pkg_resources.EntryPoint.parse('x={}'.format(name))
    result = entry_point.load(False)
    return result

class Affordance():
    def __init__(self, id, entry_point=None, cached=False, cache_length = None, **kwargs):
        self.id = id
        self.entry_point = entry_point
        self.cached = cached
        self.cache_length = cache_length

        invoker = load(self.entry_point)

        self.logic = partial(invoker, **kwargs)

    def __call__(self, *params):
        return self.logic(*params)

    @property
    def _info(self):
        return NotImplemented

class Registry():
    def __init__(self):
        self.affordances = {}

    def register(self, entry_point, **kwargs):
        id = self._newid()
        self.affordances[id] = Affordance(id, entry_point, **kwargs)

    def invoke(self, id, *params):
        affordance = self._find(id)
        observations, rewards, done, info = affordance(*params)

    def _find(self, id):
        if not id in self.affordances:
            raise error.Error('Could not find affordance with id: {}'.format(id))
        else:
            return self.affordances[id]

    def _newid(self):
        counter = itertools.count()
        newid = next(counter)
        return newid

    def list_all(self):
        return NotImplemented

registry = Registry()

def register(entry_point, **kwargs):
    registry.register(entry_point, **kwargs)
