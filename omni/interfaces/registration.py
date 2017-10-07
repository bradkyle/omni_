from .core import Interface
import itertools
import pkg_resources
import re
import logging
from omni import error
logger = logging.getLogger(__name__)

env_id_re = re.compile(r'^(?:[\w:-]+\/)?([\w:.-]+)-v(\d+)$')

def affordance(inst, *args, **kwargs):
    """
    Registers an interface function as an action that the agent
    can perform in order to,
    If type task:
    Registers an interface function as a source of the instance
    rewards i.e. profit, profit/time .etc
    Rewards from every interface task are returned at every
    step of the agent instance class.
    """
    class AffordanceSpec():
        def __init__(self, interface_instance, kind="action"):
            self.interface_instance = interface_instance
            self.kind = kind

        def invoke(self):
            return NotImplementedError

    return NotImplemented

def load(name):
    entry_point = pkg_resources.EntryPoint.parse('x={}'.format(name))
    result = entry_point.load(False)
    return result

class InterfaceSpec():
    def __init__(self, id,  tags=None, entry_point=None, kwargs=None, reward_threshold=None, local_only=False, nondeterministic=True,):
        self.id = id

        self.reward_threshold = reward_threshold

        # Environment properties
        self.nondeterministic = nondeterministic

        if tags is None:
            tags = {}
        self.tags = tags

        match = env_id_re.search(id)
        if not match:
            raise error.Error(
                'Attempted to register malformed environment ID: {}. (Currently all IDs must be of the form {}.)'.format(
                    id, env_id_re.pattern))
        self._env_name = match.group(1)
        self._entry_point = entry_point
        self._local_only = local_only
        self._kwargs = {} if kwargs is None else kwargs

    def make(self, seed):
        """Instantiates an instance of the environment with appropriate kwargs"""
        if self._entry_point is None:
            raise error.Error('Attempting to make deprecated env {}. (HINT: is there a newer registered version of this env?)'.format(self.id))

        elif callable(self._entry_point):
            env = self._entry_point()
        else:
            cls = load(self._entry_point)
            env = cls(**self._kwargs + seed)

        # Make the enviroment aware of which spec it came from.
        env.unwrapped._spec = self

        return env

class Registry():
    def __init__(self):
        self.interface_specs = {}

    def spawn(self, seed, instance):
        for interface_seed in seed["interfaces"]:
            logger.info('Spawning affordances in : %s', interface_seed["id"])
            spec = self.spec(interface_seed["id"])
            interface = spec.make(interface_seed)
            if (interface.spec.timestep_limit is not None) and not spec.tags.get('vnc'):
                from gym.wrappers.time_limit import TimeLimit
                interface = TimeLimit(interface,
                                max_episode_steps=interface.spec.max_episode_steps,
                                max_episode_seconds=interface.spec.max_episode_seconds)
            instance.interfaces[interface_seed["id"]] = interface
            self._build(instance)

    def _build(self, instance):
        instance.affordances = {}
        instance.tasks = {}

    def all(self):
        return self.interface_specs.values()

    def spec(self, id):
        match = env_id_re.search(id)
        if not match:
            raise error.Error(
                'Attempted to look up malformed interface ID: {}. (Currently all IDs must be of the form {}.)'.format(
                    id.encode('utf-8'), env_id_re.pattern))
        try:
            return self.interface_specs[id]
        except KeyError:
            # Parse the env name and check to see if it matches the non-version
            # part of a valid env (could also check the exact number here)
            env_name = match.group(1)
            matching_envs = [valid_env_name for valid_env_name, valid_env_spec in self.interface_specs.items()
                             if env_name == valid_env_spec._env_name]
            if matching_envs:
                raise error.DeprecatedEnv('Interface {} not found (valid versions include {})'.format(id, matching_envs))
            else:
                raise error.UnregisteredEnv('No registered env with id: {}'.format(id))

    def register(self, id, **kwargs):
        if id in self.interface_specs:
            raise error.Error('Cannot re-register id: {}'.format(id))
        self.interface_specs[id] = InterfaceSpec(id, **kwargs)




registry = Registry()


def register(id, **kwargs):
    return registry.register(id, **kwargs)

def spawn(seed, instance):
    if seed is not None:
        return registry.spawn(seed, instance)
    else:
        raise Exception

def spec(id):
    return registry.spec(id)

