import gym
import numpy as np
from gym import error, spaces
import itertools
import uuid


class OmniCore():
    def __init__(self):
        raise NotImplementedError

class Omni():
    def __init__(self, guru_on = True):
        self.instances = {}
        self.guru_on = guru_on
        self.id_len = 10
        self.line_length = 1024 #todo change
        self.padding_char = " "
        self.char_embedding = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}\n"


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
                raise NotImplementedError

            def _get_reward(self):
                return NotImplementedError

            @property
            def action_space(self):
                return self.omni.action_space(self.instance_id)

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

    def penalize(self):
        return NotImplementedError

    def action_space(self, instance_id):
        return spaces.Tuple(
            spaces.Box(low=0, high=len(self.interfaces), shape=1),
            spaces.Box(low=-180, high=180, shape=1))

    def observation_space(self):
        return NotImplementedError

    def reward_space(self):
        return NotImplementedError

    def encode(self, observation):
        """
        Encodes the observation response with a char embedding
        that is the same across all instances.
        """
        result = []
        for line in observation:
            line = list(line)
            if len(line) > self.line_length:
                line = line[-self.line_length:]
            num_padding = self.line_length - len(line)
            output_line = line + [self.padding_char] * num_padding
            result.append(np.array([self.char_embedding.find(char) for char in output_line], dtype=np.int8))
        return result

class Guru():
    def __init__(self):
        return NotImplementedError