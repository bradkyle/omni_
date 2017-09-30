class Account(object):
    def __init__(self, agent, index, balances, status):
        self.agent = agent
        self.index = index
        self.balances = balances
        self.status = status
        self.pseudo_balance = 0.0
        self.enabled = True

    def buy(self):
        return NotImplemented

    def sell(self):
        return NotImplemented

    def seed(self):
        return NotImplementedError

    def reset(self):
        return NotImplementedError

    def close(self):
        return NotImplementedError


class Balance():
    def __init__(self, asset, amount):
        self.asset = asset
        self.amount = amount
        self.available_amount = amount
        self.hold_amount = 0.0


