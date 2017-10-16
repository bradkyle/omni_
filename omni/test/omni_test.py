import unittest
from omni.omni import Omni
import pytest
from omni.interfaces import register
import json



register(
    enabled=False,
    id='Interfacer-v0',
    entry_point='omni.test.test_interface:Interfacer'
)


class TestOmni(unittest.TestCase):
    def setUp(self):
        self.omni = Omni()

    def test_instantiate(self):
        instance = self.omni.instantiate()

class TestInstance(unittest.TestCase):

    def setUp(self):
        self.omni = Omni()
        self.test_seed = self._test_seed()

    def test_seed(self):
        instance = self.omni.instantiate()
        instance.seed(seed=self.test_seed)
        self.assertEqual(instance.interfaces["Interfacer-v0"].test_key, "test_value")

    def test_close(self):
        instance = self.omni.instantiate()

    def test_reset(self):
        instance = self.omni.instantiate()

    def test_lookup(self):
        instance = self.omni.instantiate()

    def test_step(self):
        instance = self.omni.instantiate()
        instance.seed(seed=self.test_seed)





        action = instance.action_space.sample()
        ob, reward, done, _ = instance.step(action)
        self.assertEqual(ob, "test_observation")
        self.assertEqual(reward, 189)
        self.assertEqual(done, 189)


    def test_aggregate_rewards(self):
        instance = self.omni.instantiate()

    def _test_seed(self):
        json_data = """{
          "interfaces":[
            {
              "id": "Interfacer-v0",
              "args": {
                "test_key": "test_value"
              }
            }
          ]
        }"""
        d = json.loads(json_data)
        return d

if __name__ == '__main__':
    unittest.main()