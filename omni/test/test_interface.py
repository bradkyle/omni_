from omni.interfaces.core import Interface
from omni.interfaces.registration import afford



class Interfacer(Interface):
    interface_id = "Interfacer-v0"

    permutations = ["bam","mab","huy"]

    def __init__(self, test_key, enabled=True):
        self.enabled = enabled
        self.test_key = test_key
        self.bam = "bam"

    def _invoke(self, params):
        return NotImplemented

    def _close(self):
        return NotImplemented

    @property
    def test_affordance(self):
        return "test_observation"

    @afford
    def test_permutation_affordance(self, permutation):
        return permutation

    @afford
    def test_task(self):
        return 189
