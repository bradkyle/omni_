import argparse
import numpy as np
import time

from omni.interfaces.registration import affordance_registry,task_registry, closer_registry

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
    affordance(0.01, 0.1)

def test_close():
    affordance = affordance_registry.lookup(id)
    affordance()

def test_tasks():
    rewards = task_registry.aggregate()
    print(rewards)
    time.sleep(60)
    rewards = task_registry.aggregate()
    print(rewards)
    flattened_rewards = np.hstack(rewards)
    print(flattened_rewards)

    closer_registry.close()

def test_single_task(id):
    if id in task_registry.tasks:
        task = task_registry.tasks[id]
    else:
        raise Exception
    task()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--func', help='function to execute', default="lista")
    parser.add_argument('--aff', help='affordance ID', default=140)
    parser.add_argument('--tsk', help='task ID', default=None)
    args = parser.parse_args()

    if args.func == "lista":
        list_affordances()
    elif args.func == "testa":
        test_affordances(211)
    elif args.func == "listsk":
        list_tasks()
    elif args.func == "testsk":
        if args.tsk:
            test_single_task(args.tsk)
        else:
            test_tasks()



if __name__ == '__main__':
    main()