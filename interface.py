import itertools
from omni.error import NoEntryPointError, NoneResponseError, TypeNotFoundError, InputTypeNotFoundError
import pkg_resources
from enum import Enum

class TYPE(Enum):
    AFFORDANCE = 1
    FEATURE = 2
    TASK = 3
    CLOSER = 4
    INFO = 5
    OBJECTIVE = 6
    CONFIG = 7

class STATE(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DISABLED = 3
    ENABLED = 4

# Interfaces
# =====================================================================================================================>

# todo make alert and deactivate on error handler

class Input():
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.args = None

# todo apply rate limit at the interface level

class Interface():
    """
    An interface in this instance is an entity which specifies a mode of interaction
    with a service.
    """

    # interface id generation
    id = itertools.count(start=0,step=1)

    def _reset(self):
        self.id = itertools.count(start=0,step=1)

    def __init__(self, type, entry_point, state=STATE.ACTIVE, title=None, description=None, **kwargs):
        if entry_point is None or "":
            raise NoEntryPointError

        if type not in TYPE:
            raise TypeNotFoundError

        self.id = next(self.id)
        self.type = type
        self.state = state
        self.entry_point = entry_point
        self.invoker = load(self.entry_point)
        self.input = Input(**kwargs)

        if not hasattr(self.input, 'rate_limit'):
            self.input.rate_limit = 2

        self.title = title
        self.description = description

    # todo define interface type by instance configuration
    def __call__(self, *params, input_kind=None):
        self.input.args = params
        return self.invoker(self.input)

    async def switch_state(self, state):
        if state in STATE:
            self.state = state
        else:
            raise TypeError("Incorrect interface state type was provided '"+str(state)+"'")



def interface(func):
    def expose_core(*args, **kwargs):
        return func(*args, **kwargs)
    return expose_core

# returns observation, features, success,


# Utils
def load(name):
    entry_point = pkg_resources.EntryPoint.parse('x={}'.format(name))
    result = entry_point.load(False)
    return result