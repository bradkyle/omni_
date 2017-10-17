from omni.interfaces.registration import affordance_registry

def test():
    print("TESTING")

    # affordance = affordance_registry.lookup(1)
    # print(affordance.entry_point)

    for affordance in affordance_registry.affordances.values():
        print(affordance.entry_point + ": ")

    action = affordance_registry.affordances[1]

    print(action())

if __name__ == '__main__':
    test()
