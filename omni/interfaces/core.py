import numpy as np
import requests
from omni.error import DoubleWrapperError




class Response():
    def __init__(self):
        raise NotImplemented




class Interface():
    """
    The main Omniverse Interface class. It encapsulates an interface with arbitrary
    behind-the-scenes dynamics.

    Interfaces form what is in essence the entire omniverse environment.
    Interfaces afford opp

    Essentially takes in an array of continuous actions and converts those continuous actions into
    parameters that compose a specific invocation of an external entity, by whatever protocol.
    In this case http is implemented, although more protocols will be implemented in the future.

    An instance of an interface is in essence a connection between an agent and an external
    interactive entity. This can then be parametrised with values representative of that
    agent such as authentication keys .etc
    """
    def __new__(cls, *args, **kwargs):
        # We use __new__ since we want the entity interface to be able to
        # override __init__ without having to call super.
        interface = super(Interface, cls).__new__(cls)
        interface._spec = None

        # Will be automatically set when creating an environment via 'make'
        return interface

    # Override in ALL subclasses
    def _invoke(self, params): raise NotImplementedError
    def _close(self): raise NotImplementedError

    def invoke(self, params):
        return self._invoke(params)

    def close(self):
        self._close()

    def cache(self):
        return NotImplemented

    @property
    def spec(self):
        return self._spec

    @property
    def unwrapped(self):
        """Completely unwrap this env.

        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self

    def __del__(self):
        self.close()


class Space(object):
    """
    Defines the observation and action spaces, so you can write generic
    code that applies to any Env. For example, you can choose a random
    action.
    """
    def sample(self):
        """
        Uniformly randomly sample a random element of this space
        """
        raise NotImplementedError

    def contains(self, x):
        """
        Return boolean specifying if x is a valid
        member of this space
        """
        raise NotImplementedError

    def to_jsonable(self, sample_n):
        """Convert a batch of samples from this space to a JSONable data type."""
        # By default, assume identity is JSONable
        return sample_n

    def from_jsonable(self, sample_n):
        """Convert a JSONable data type to a batch of samples from this space."""
        # By default, assume identity is JSONable
        return sample_n

class Wrapper(Interface):
    # Clear metadata so by default we don't override any keys.
    metadata = {}
    _owns_render = False
    # Make sure self.env is always defined, even if things break
    # early.
    env = None

    def __init__(self, env):
        self.env = env
        # Merge with the base metadata
        metadata = self.metadata
        self.metadata = self.env.metadata.copy()
        self.metadata.update(metadata)

        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.reward_range = self.env.reward_range
        self._ensure_no_double_wrap()

    @classmethod
    def class_name(cls):
        return cls.__name__

    def _ensure_no_double_wrap(self):
        env = self.env
        while True:
            if isinstance(env, Wrapper):
                if env.class_name() == self.class_name():
                    raise DoubleWrapperError("Attempted to double wrap with Wrapper: {}".format(self.__class__.__name__))
                env = env.env
            else:
                break

    def _step(self, action):
        return self.env.step(action)

    def _reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def _render(self, mode='human', close=False):
        return self.env.render(mode, close)

    def _close(self):
        if self.env:
            return self.env.close()

    def _seed(self, seed=None):
        return self.env.seed(seed)

    def __str__(self):
        return '<{}{}>'.format(type(self).__name__, self.env)

    def __repr__(self):
        return str(self)

    @property
    def unwrapped(self):
        return self.env.unwrapped

    @property
    def spec(self):
        return self.env.spec

class ObservationWrapper(Wrapper):
    def _reset(self, **kwargs):
        observation = self.env.reset(**kwargs)
        return self._observation(observation)

    def _step(self, action):
        observation, reward, done, info = self.env.step(action)
        return self.observation(observation), reward, done, info

    def observation(self, observation):
        return self._observation(observation)

    def _observation(self, observation):
        raise NotImplementedError

class RewardWrapper(Wrapper):
    def _step(self, action):
        observation, reward, done, info = self.env.step(action)
        return observation, self.reward(reward), done, info

    def reward(self, reward):
        return self._reward(reward)

    def _reward(self, reward):
        raise NotImplementedError

class ActionWrapper(Wrapper):
    def _step(self, action):
        action = self.action(action)
        return self.env.step(action)

    def action(self, action):
        return self._action(action)

    def _action(self, action):
        raise NotImplementedError

    def reverse_action(self, action):
        return self._reverse_action(action)

    def _reverse_action(self, action):
        raise NotImplementedError
