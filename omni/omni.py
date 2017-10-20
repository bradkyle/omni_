import gym
import numpy as np
from gym import error, spaces
import itertools
import uuid
from omni.interfaces.registration import affordance_registry, task_registry, closer_registry
from omni.config import MAX_PARAMS, LINE_LENGTH, CHAR_EMBEDDING


class Omni():
    def __init__(self):
        self.instances = {}
        self.id_len = 10

    def instantiate(self):
        """
        Creates an instance connection for an agent
        """
        class Instance(gym.Env):
            omni = self
            def __init__(self, instance_id):
                self.instance_id = instance_id
                self.step_count = 0
                self.done = False

            def _close(self):
                closer_registry.close()

            def _seed(self, seed=None):
               return NotImplementedError

            def _step(self, action):
                affordance = affordance_registry.lookup(action[0])
                self.observation, self.penalty = affordance(action[1])
                self.reward = task_registry.aggregate()
                self.step_count += 1
                return self.observation, self.penalty + self.reward, self.done, self.info

            @property
            def info(self):
                return {
                    'step': self.step_count
                }

            @property
            def action_space(self):
                return self.omni.action_space

            @property
            def observation_space(self):
                return self.omni.observation_space

            @property
            def reward_space(self):
                return self.omni.reward_space

        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        instance = Instance(instance_id)
        self.instances[instance_id] = instance
        return instance

    def observation_space(self):
        spaces.Box(low=0, high=len(CHAR_EMBEDDING)+1, shape=(LINE_LENGTH))

    def reward_space(self):
        return spaces.Tuple((spaces.Box(low=-100, high=100, shape=1),
                            spaces.Box(low=-100, high=100, shape=len(task_registry.list_all))))

    def action_space(self):
        return spaces.Tuple((spaces.Discrete(len(affordance_registry.list_all)),
                            spaces.Box(low=0, high=1, shape=MAX_PARAMS)))

