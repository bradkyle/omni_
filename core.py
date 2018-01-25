from enum import Enum
from omni.error import InterfaceNotFoundError
from heapq import nsmallest
import numpy as np
from omni.interface import Interface, TYPE

# Utils
# =====================================================================================================================>



class OUTPUT(Enum):
    RESPONSE_ONLY = 1
    FEATURES_ONLY = 2
    HYBRID = 3

class STAGE(Enum):
    DEVELOPMENT = 1
    TRAINING = 2
    EVALUATION = 3
    PRODUCTION = 4

class METHOD(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    UPDATE = 4
    HEAD = 5
    OPTIONS = 6

# Core
# =====================================================================================================================>

# todo make persistent
class Registry():

    def __init__(self):
        # Registry
        self.interface_registry = {} # todo change to entity registry ?
        self.interface_list=[]

    def count(self, type=None):
        if type is None:
            return len(self.interface_registry)
        else:
            return len([v for k,v in self.interface_registry.items() if v.type == type])

    async def sample(self, type=None):
        if type is None:
            return np.random.choice(self.interface_registry.keys())
        else:
            return np.random.choice([k for k,v in self.interface_registry.items() if v.type == type])

    async def flush(self):
        self.interface_registry = {}

    def register(self, type, entry_point,  title=None, description=None, **kwargs):
        interface = Interface(type, entry_point,  title=title, description=description,**kwargs)
        self.interface_registry[interface.id] = interface
        return True

    async def lookup(self, index):
        if index in self.interface_registry:
            interface = self.interface_registry[index]
            return interface
        else:
            raise InterfaceNotFoundError

    async def list_entrypoint(self, entry_point, state=None):
        if state is None:
            result = [k for k, v in self.interface_registry.items() if v.entry_point == entry_point]
        else:
            result = [k for k, v in self.interface_registry.items() if v.entry_point == entry_point and v.state == state]
        return result

    async def list_type(self, type, state=None):
        if state is None:
            result = [v for k,v in self.interface_registry.items() if v.type == type]
        else:
            result = [v for k, v in self.interface_registry.items() if v.type == type and v.state == state]
        return result

    async def dict_type(self, type, state=None):
        if state is None:
            result = {k: v for k, v in self.interface_registry.items() if v.type == type}
        else:
            result = {k: v for k, v in self.interface_registry.items() if v.type == type and v.state == state}
        return result

    async def list_all(self, state=None):
        result = [v for k, v in self.interface_registry.items()]
        return result

registry = Registry()

async def count(type=None):
    return registry.count(type=type)

async def list_all_interfaces():
    return await registry.list_all()

async def list_all_interface_info(): # todo complete
    return await registry.list_all()

# should return an array of action indicies
# spawns an array of interfaces through the agent can actively interact with the outside world
async def spawn_candidates(index, k):
    affordances = await registry.dict_type(TYPE.AFFORDANCE)
    candidates = nsmallest(k, affordances, key=lambda x: abs(x - int(index)))
    return candidates

async def scale_index(index, max=1, min=0, type=TYPE.AFFORDANCE):
    assert min < index < max
    interface_count = registry.count(type=type)
    return index*(interface_count * max)

async def cont_execute(index, args):
    interface = await registry.lookup(index)
    response = await interface(*args)
    return response

# should return an 1D encoded observation list
async def disc_execute(index):
    interface = await registry.lookup(index)
    assert interface.type == TYPE.AFFORDANCE
    result = await interface()
    return result

async def execute_multiple_by_index(indicies):
    result = []
    for index in indicies:
        interface = await registry.lookup(index)
        result.append(await interface())
    return result

async def execute_multiple(interfaces):
    result = []
    for interface in interfaces:
        result.append(await interface())
    return result

# should return a list of rewards
async def aggregate_tasks(range=None):
    interfaces = await registry.list_type(TYPE.TASK)
    response = await execute_multiple(interfaces)
    result = np.array(response)
    result = result.flatten()
    return result

# should return an array of dicts with information
async def aggregate_info():
    interfaces = await registry.list_type(TYPE.INFO)
    result = await execute_multiple(interfaces)
    return result

async def aggregate_features(range=None):
    interfaces = await registry.list_type(TYPE.FEATURE)
    result = await execute_multiple(interfaces)
    return result

# should execute multiple closing interfaces
async def execute_closers():
    closers = await registry.list_type(TYPE.CLOSER)
    await execute_multiple(closers)
    return

async def config():
    raise NotImplemented

async def get_config():
    raise NotImplemented

def register(type, entry_point, title=None, description=None,**kwargs):
    registry.register(type, entry_point, title=title, description=description, **kwargs)


class SubRegistry():
    def __init__(self):
        self.interface_registry = {}




