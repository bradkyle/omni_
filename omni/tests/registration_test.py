import argparse
import numpy as np
import time

from omni.interfaces.registration import affordance_registry,task_registry

# Registration Tests
#---------------------------------------------------------------------------------------------------------------------->

def afford():
    affordance = affordance_registry.lookup(97)
    affordance(0.001, 0.001)

# Registration Tests
#---------------------------------------------------------------------------------------------------------------------->

def list_affordances():
    reg = affordance_registry.affordances.values()
    for affordance in reg:
       print(str(affordance.id)+ ': ' +affordance.entry_point)

def list_tasks():
    ret = task_registry.tasks.values()
    for task in ret:
        print(task.entry_point)

def test_affordances(id):
    affordance = affordance_registry.lookup(id)
    affordance()

def test_close():
    affordance = affordance_registry.lookup(id)
    affordance(0.1, 0.1)

def test_tasks():
    rewards = task_registry.aggregate()
    print(rewards)
    time.sleep(60)
    rewards = task_registry.aggregate()
    print(rewards)
    flattened_rewards = np.hstack(rewards)
    print(flattened_rewards)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--aff', help='affordance ID', default=1)
    args = parser.parse_args()
    test_affordances(args.aff)


if __name__ == '__main__':
    test_tasks()
    #list_tasks()
    # test_affordances(0)
    # list_affordances()