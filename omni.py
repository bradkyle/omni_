import gym
import numpy as np
from gym import error, spaces
import itertools
import uuid
from omni.core import registry, spawn_candidates, aggregate_tasks, cont_execute, execute_closers, TYPE, STATE, SubRegistry
import tensorflow as tf
import omni.config
import six
import json
from heapq import nsmallest

# todo implement safe shutdown
# todo add support for running omni on a seperate thread

# Omni
# =====================================================================================================================>

class Omni():
    def __init__(self):
        self.instances = {}
        self.id_len = 10

    def instantiate(self, config=None, direct=True):
        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        instance = Instance(instance_id, config)
        self.instances[instance_id] = instance
        if direct:
            return instance
        else:
            return instance.instance_id

    def list_instances(self):
        return dict([(instance_id, instance.config) for (instance_id, instance) in self.instances.items()])

    def lookup(self, instance_id):
        try:
            return self.instances[instance_id]
        except KeyError:
            raise Exception

    def remove(self, instance_id):
        try:
            del self.instances[instance_id]
        except KeyError:
            raise Exception

    def spawn_candidates(self, instance_id, k, index):
        instance = self.lookup(instance_id)
        candidates = instance.spawn_candidates(k, index)
        return candidates

    def instance_close(self, instance_id):
        instance = self.lookup(instance_id)
        instance.close()
        self.remove(instance_id)

    def reset(self, instance_id):
        instance = self.lookup(instance_id)
        obs = instance.reset()
        return instance.observation_space.to_jsonable(obs)

    def step(self, instance_id, action, render):
        instance = self.lookup(instance_id)
        if isinstance(action, six.integer_types):
            nice_action = action
        else:
            nice_action = np.array(action)
        if render:
            instance.render()
        [observation, reward, done, info] = instance.step(nice_action)
        obs_jsonable = instance.observation_space.to_jsonable(observation)
        return [obs_jsonable, reward, done, info]


    def get_action_space_contains(self, instance_id, x):
        instance = self.lookup(instance_id)
        return instance.action_space.contains(int(x))

    def get_action_space_info(self, instance_id):
        instance = self.lookup(instance_id)
        return self._get_space_properties(instance.action_space)

    def get_action_space_sample(self, instance_id):
        instance = self.lookup(instance_id)
        action = instance.action_space.sample()
        if isinstance(action, (list, tuple)) or ('numpy' in str(type(action))):
            try:
                action = action.tolist()
            except TypeError:
                print(type(action))
                print('TypeError')
        return action

    def get_observation_space_contains(self, instance_id, j):
        instance = self.lookup(instance_id)
        info = self._get_space_properties(instance.observation_space)
        for key, value in j.items():
            # Convert both values to json for comparibility
            if json.dumps(info[key]) != json.dumps(value):
                print('Values for "{}" do not match. Passed "{}", Observed "{}".'.format(key, value, info[key]))
                return False
        return True

    def get_observation_space_info(self, instance_id):
        instance = self.lookup(instance_id)
        return self._get_space_properties(instance.observation_space)

    def _get_space_properties(self, space):
        info = {}
        info['name'] = space.__class__.__name__
        if info['name'] == 'Discrete':
            info['n'] = space.n
        elif info['name'] == 'Box':
            info['shape'] = space.shape
            # It's not JSON compliant to have Infinity, -Infinity, NaN.
            # Many newer JSON parsers allow it, but many don't. Notably python json
            # module can read and write such floats. So we only here fix "export version",
            # also make it flat.
            info['low']  = [(x if x != -np.inf else -1e100) for x in np.array(space.low ).flatten()]
            info['high'] = [(x if x != +np.inf else +1e100) for x in np.array(space.high).flatten()]
        elif info['name'] == 'HighLow':
            info['num_rows'] = space.num_rows
            info['matrix'] = [((float(x) if x != -np.inf else -1e100) if x != +np.inf else +1e100) for x in np.array(space.matrix).flatten()]
        return info



# Instance
# =====================================================================================================================>

# todo add instance specific config
class Instance(gym.Env):
    def __init__(self, instance_id, config=None):
        self.instance_id = instance_id
        self.instance_interfaces = SubRegistry()
        self.done = False
        self.config(config)

    def _close(self):
        print("Close: Not Implemented yet!")

    def _reset(self):
        return self.observation_space.sample()

    def _render(self, mode='human', close=False):
        print("Render: Not Implemented yet!")

    def _seed(self, seed=None):
        return Warning("Cannot seed live environment")

    async def step(self, index_action, param_action):
        observation = await cont_execute(index_action, param_action)
        rewards = await aggregate_tasks()
        done = await self.is_done
        info = None
        return observation, rewards, info, done

    async def multi_step(self, actions):
        return NotImplemented

    def config(self, config):
        return NotImplemented

    async def randomize(self):
        return NotImplemented

    async def randomize_affordance_indicies(self):
        affordance_count = registry.count()
        nums = np.ones(affordance_count)
        nums[:affordance_count * 0.3] = 1
        return np.random.shuffle(nums)

    def spawn_candidates(self, k, index):
        affordances = registry.dict_type(TYPE.AFFORDANCE)
        candidates = nsmallest(k, affordances, key=lambda x: abs(x - int(index)))
        return candidates

    @property
    def action_space(self):
        return spaces.Box(low=-1, high=1, shape=(4))

    @property
    def observation_space(self):
        return spaces.Box(low=-5, high=5, shape=(3000, 96, 1))

    @property
    def reward_space(self):
        return spaces.Box(low=-100, high=100, shape=(9))

    @property
    async def is_done(self):
        return False

    @property
    def defaults(self):
        return omni.config.instance_defaults





