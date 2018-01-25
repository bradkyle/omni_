from omni import Instance
import numpy as np

class TestInstance(Instance):

    def __init__(self,instance_id,config):
        Instance.__init__(self,instance_id,config)

    async def step(self, test_reward_space=None, test_observation_space=None):
        if test_reward_space is None:
            observation = self.observation_space.sample()
        else:
            observation = np.random.randint(high=test_observation_space.high,
                                            low=test_observation_space.low,
                                            size=test_observation_space.shape)

        if test_reward_space is None:
            rewards = self.reward_space.sample()
        else:
            rewards = np.random.randint(high=test_reward_space.high,
                                        low=test_reward_space.low,
                                        size=test_reward_space.shape)

        done = False
        info = None
        return observation, rewards, info, done

