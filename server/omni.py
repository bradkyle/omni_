import gym


class Omni():
    def __init__(self):
        self.instances = {}

    def instantiate(self):
        class Instance(gym.Env):
            def __init__(self):
                raise NotImplementedError

            def close(self):
                return NotImplementedError

            def seed(self):
                return NotImplementedError

            def render(self):
                return NotImplementedError

            def reset(self):
                return NotImplementedError

            def step(self, instance_id, action):
                raise NotImplementedError

            @property
            def action_space(self):
                return NotImplementedError

            @property
            def observation_space(self):
                return NotImplementedError

            @property
            def reward_space(self):
                return NotImplementedError


    def vertex(self):
        return NotImplementedError

    def connection(self):
        return NotImplementedError

    def encode(self):
        return NotImplementedError

