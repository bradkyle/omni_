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

class AffordanceRegistry():
    def __init__(self):
        self.affordances = {}
        self.id_counter = 0

    def register(self, entry_point, **kwargs):
        self.affordances[self.id_counter] = Affordance(id, entry_point, **kwargs)
        self.id_counter += 1

    def lookup(self, id):
        return self._find(id)

    def invoke(self, id, *params):
        affordance = self._find(id)
        observations, rewards, done, info = affordance(*params)

    def _find(self, id):
        if not id in self.affordances:
            raise error.Error('Could not find affordance with id: {}'.format(id))
        else:
            return self.affordances[id]

    def all(self):
        return self.affordances.values()

affordance_registry = AffordanceRegistry()

def register(entry_point, **kwargs):
    affordance_registry.register(entry_point, **kwargs)

class Task():
    def __init__(self, invoker, per_step=None, **kwargs):
        self.per_step = per_step
        self.invoker = invoker
        self.kwargs = kwargs

    def __call__(self):
       return self.invoker(self.kwargs)

class TaskRegistry():
    def __init__(self):
        self.tasks = {}

    def task(self, entry_point, **kwargs):
        return NotImplemented

    def aggregate(self):
        return NotImplemented


task_registry = TaskRegistry()

def task(entry_point, **kwargs):
    task_registry.task(entry_point, **kwargs)
