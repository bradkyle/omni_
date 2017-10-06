import gym
import numpy as np
from gym import error, spaces
import itertools
import uuid
from omni.interfaces.registration import omnispawn, lookup_affordance


class OmniCore():
    def __init__(self):
        raise NotImplementedError

class Omni():
    def __init__(self):
        self.instances = {}
        self.id_len = 10
        self.done = False

    def instantiate(self):
        """
        Creates an instance connection for an agent
        """
        class Instance(gym.Env):
            omni = self
            def __init__(self, instance_id):
                self.instance_id = instance_id

            def _close(self):
                return NotImplementedError

            def _seed(self, seed=None):
                return NotImplementedError

            def _render(self, mode='human', close=False):
                return NotImplementedError

            def _reset(self):
                return NotImplementedError

            def _step(self, action):
                affordance = lookup_affordance(action[0])
                self.observation = affordance.invoke(action[1])
                self.reward = self.aggregate_rewards()
                return self.observation, self.reward, self.done, self.info

            def aggregate_rewards(self):
                return NotImplemented

            @property
            def done(self):
                return NotImplemented

            @property
            def info(self):
                return NotImplemented

            @property
            def action_space(self):
                return self.omni.action_space(self.instance_id)

            @property
            def observation_space(self):
                return self.omni.observation_space()

            @property
            def reward_space(self):
                return self.omni.reward_space()

        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        instance = Instance(instance_id)
        self.instances[instance_id] = instance
        return instance

    def action_space(self, instance_id):
        return spaces.Tuple(
            spaces.Box(low=0, high=self.action_space_size, shape=1),
            spaces.Box(low=-180, high=180, shape=1))

    def observation_space(self):
        return NotImplementedError

    def reward_space(self):
        return NotImplementedError

    @property
    def action_space_size(self):
        return len(self.affordances)
