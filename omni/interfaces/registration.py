from .core import Interface
import itertools
import pkg_resources
import re
import logging
from omni import error
logger = logging.getLogger(__name__)

interface_id_re = re.compile(r'^(?:[\w:-]+\/)?([\w:.-]+)-v(\d+)$')

def load(name):
    entry_point = pkg_resources.EntryPoint.parse('x={}'.format(name))
    result = entry_point.load(False)
    return result

class InterfaceSpec():
    def __init__(self, id, enabled=True, trials=100, rate_limit=None, cached=None, cache_length = None, tags=None, entry_point=None, kwargs=None, reward_threshold=None, local_only=False, nondeterministic=True, max_episode_steps=None, max_episode_seconds=None, timestep_limit=None):
        self.id = id

        self.reward_threshold = reward_threshold
        self.timestep_limit = timestep_limit
        self.timestep_limit = timestep_limit
        self.max_episode_steps = max_episode_steps
        self.max_episode_seconds = max_episode_seconds
        self.nondeterministic = nondeterministic

        if tags is None:
            tags = {}
        self.tags = tags

        match = interface_id_re.search(id)
        if not match:
            raise error.Error(
                'Attempted to register malformed interface ID: {}. (Currently all IDs must be of the form {}.)'.format(
                    id, interface_id_re.pattern))
        self._interface_name = match.group(1)
        self._entry_point = entry_point
        self._local_only = local_only
        self._kwargs = {} if kwargs is None else kwargs

    def make(self, seed):

        if seed is None:
            seed = {}
        self._kwargs.update(seed)


        """Instantiates an instance of the interface with appropriate kwargs"""
        if self._entry_point is None:
            raise error.Error('Attempting to make deprecated interface {}. (HINT: is there a newer registered version of this interface?)'.format(self.id))

        elif callable(self._entry_point):
            interface = self._entry_point()
        else:
            cls = load(self._entry_point)
            interface = cls(**self._kwargs)

        # Make the interface aware of which spec it came from.
        interface.unwrapped._spec = self

        return interface

class AffordanceSpec():
    def __init__(self, interface,  func, requires=None, kind="action"):
        self.interface = interface
        self.kind = kind
        self.func = func
        if requires is None:
            self.requires = {}
        else:
            self.requires = requires

    def __call__(self):
        return NotImplemented

class Registry():
    def __init__(self):
        self.interface_specs = {}

    def spawn(self, seed, instance):
        instance.interfaces = {}
        if seed is not None:
            for interface_seed in seed["interfaces"]:
                spec = self.spec(interface_seed["id"])
                interface = spec.make(interface_seed["args"])

                if (interface.spec.timestep_limit is not None) and not spec.tags.get('vnc'):
                    from gym.wrappers.time_limit import TimeLimit
                    interface = TimeLimit(interface,
                                    max_episode_steps=interface.spec.max_episode_steps,
                                    max_episode_seconds=interface.spec.max_episode_seconds)

                instance.interfaces[interface_seed["id"]] = interface

        setAffordances(instance)
        return


    def all(self):
        return self.interface_specs.values()

    def spec(self, id):
        match = interface_id_re.search(id)
        if not match:
            raise error.Error(
                'Attempted to look up malformed interface ID: {}. (Currently all IDs must be of the form {}.)'.format(
                    id.encode('utf-8'), interface_id_re.pattern))
        try:
            return self.interface_specs[id]
        except KeyError:
            # Parse the interface name and check to see if it matches the non-version
            # part of a valid interface (could also check the exact number here)
            interface_name = match.group(1)
            matching_interfaces = [valid_interface_name for valid_interface_name, valid_interface_spec in self.interface_specs.items()
                             if interface_name == valid_interface_spec._interface_name]
            if matching_interfaces:
                raise error.DeprecatedInterface('Interface {} not found (valid versions include {})'.format(id, matching_interfaces))
            else:
                raise error.UnregisteredInterface('No registered interface with id: {}'.format(id))

    def register(self, id, **kwargs):
        if id in self.interface_specs:
            raise error.Error('Cannot re-register id: {}'.format(id))
        self.interface_specs[id] = InterfaceSpec(id, **kwargs)

registry = Registry()

def makeRegisteringDecorator(foreignDecorator):
    """
        Returns a copy of foreignDecorator, which is identical in every
        way(*), except also appends a .decorator property to the callable it
        spits out.
    """
    def newDecorator(func):
        # Call to newDecorator(method)
        # Exactly like old decorator, but output keeps track of what decorated it
        R = foreignDecorator(func) # apply foreignDecorator, like call to foreignDecorator(method) would have done
        R.decorator = newDecorator # keep track of decorator
        #R.original = func         # might as well keep track of everything!
        return R

    newDecorator.__name__ = foreignDecorator.__name__
    newDecorator.__doc__ = foreignDecorator.__doc__
    # (*)We can be somewhat "hygienic", but newDecorator still isn't signature-preserving, i.e. you will not be able to get a runtime list of parameters. For that, you need hackish libraries...but in this case, the only argument is func, so it's not a big issue

    return newDecorator

def setAffordances(instance):
        """
            Returns all methods in CLS with afford as the
            outermost decorator.

            DECORATOR must be a "registering decorator"; one
            can make any decorator "registering" via the
            makeRegisteringDecorator function.
        """
        for key, cls in instance.interfaces.items():
            print(cls)
            print(dir(cls))
            for maybeDecorated in cls.__dict__.values():
                print(maybeDecorated)
                if hasattr(maybeDecorated, 'afford'):
                    print("hello")
                    if maybeDecorated.decorator == afford:
                        instance.affordances.append(maybeDecorated)
                        print(len(instance.affordances))


def afford(kind, *args, **kwargs):
    """
    Registers an interface function as an action that the agent
    can perform in order to,
    If type task:
    Registers an interface function as a source of the instance
    rewards i.e. profit, profit/time .etc
    Rewards from every interface task are returned at every
    step of the agent instance class.
    Returns a copy of foreignDecorator, which is identical in every
    way(*), except also appends a .decorator property to the callable it
    spits out.
    """
    def wrapper(func):
        def register(inst, *args, **kwargs):
            return func(inst, *args, **kwargs)
        return register
    return wrapper

afford = makeRegisteringDecorator(afford)

def register(id, **kwargs):
    return registry.register(id, **kwargs)

def spawn(seed, instance):
    return registry.spawn(seed, instance)

def spec(id):
    return registry.spec(id)

