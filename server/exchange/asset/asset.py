class Asset():
    def __init__(self, symbol, kind=None, name=None, fee=None):
        self.symbol = symbol
        self.name = name
        self.type = kind
        self.fee = fee
        self.enabled = True

