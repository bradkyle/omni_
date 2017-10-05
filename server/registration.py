import error
import itertools

class Interface():
    def __init__(self, interface_id, entry_point=None, cache=False, session=False):
        self.interface_id = interface_id

    def make(self):
        return NotImplementedError

    def setup(self):
        return NotImplementedError

    def invoke(self):
        return NotImplementedError




class InterfaceRegistry():
    def __init__(self):
        self.interfaces = {}
        self.store = {}

    def register(self, group_id, **kwargs):
        interface_id = itertools.count().next()
        self.interfaces[interface_id] = Interface(interface_id, **kwargs)



registry = InterfaceRegistry()

def register(group_id, **kwargs):
    return registry.register(group_id, **kwargs)

def permutate():
    return NotImplementedError


register(

)