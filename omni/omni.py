import gym
import numpy as np
from gym import error, spaces
import itertools
import uuid
from omni.interfaces.registration import spawn
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
                for interface in self.interfaces:
                    interface.close()

            def _seed(self, seed=None):
               spawn(seed, self)

            def _reset(self):
                for interface in self.interfaces:
                    interface.reset()

            def _lookup(self, index):
                if index in self.affordances:
                    affordance = self.affordances[index]
                    return affordance

            def _step(self, action):
                affordance = self._lookup(action[0])
                self.observation, penalty = affordance.invoke(action[1])
                self.reward = self.aggregate_rewards()
                return self.observation, self.reward, self.done, self.info

            def aggregate_rewards(self):
                rewards = []
                for task in self.tasks:
                    rewards.append(task.invoke())
                return rewards

            @property
            def done(self):
                return False

            @property
            def info(self):
                return NotImplemented

            @property
            def action_space(self):
                return spaces.Tuple(spaces.Box(low=0, high=len(self.affordances), shape=1),
                                    spaces.Box(low=-180, high=180, shape=1))

            @property
            def observation_space(self):
                return self.omni.observation_space()

            @property
            def reward_space(self):
                return spaces.Tuple(spaces.Box(low=-100, high=100, shape=1),
                                    spaces.Box(low=-100, high=100, shape=len(self.tasks)))

        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        instance = Instance(instance_id)
        self.instances[instance_id] = instance
        return instance

    def observation_space(self):
        return NotImplementedError

