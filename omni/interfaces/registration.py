from .core import Interface
import itertools

def affordance(inst, *args, **kwargs):
    """
    Registers an interface function as an action that the agent
    can perform in order to
    """
    return NotImplemented

def task(inst, *args, **kwargs):
    """
    Registers an interface function as a source of the instance
    rewards i.e. profit, profit/time .etc
    Rewards from every interface task are returned at every
    step of the agent instance class.
    """
    return NotImplemented

class InterfaceSpec():
    def __init__(self, id):
        self.id = id

    def make(self):
        return NotImplemented

class Registry():
    def __init__(self):
        self.interfaces = {}
        self.affordances = {}
        self.tasks = {}

    def omnispawn(self):
        return NotImplemented

    def all(self):
        return NotImplemented

    def spec(self, id):
        return NotImplemented

    def register(self, id, **kwargs):
        return NotImplemented

    def lookup(self, index):
        return NotImplemented

    def _sweep(self):
        return NotImplemented


registry = Registry()

def lookup_affordance(index):
    return registry.lookup(index)

def register(id, **kwargs):
    return registry.register(id, **kwargs)

def omnispawn():
    return registry.omnispawn()

def spec(id):
    return registry.spec(id)

