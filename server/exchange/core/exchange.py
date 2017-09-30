
class Exchange():
    def __new__(self):
        self.assets = []
        self.pairs = []
        self.orderbooks = []
        self.lendbooks = []
        self.accounts = []

    def new_account(self):
        return NotImplementedError

    def new_orderbook(self):
        return NotImplementedError

    def new_asset(self):
        return NotImplementedError

    def new_pair(self):
        return NotImplementedError

    def get_fee_info(self):
        return NotImplementedError

    def get_lend_book(self):
        return NotImplementedError

    def load(self):
        return NotImplementedError

    def reload(self):
        return NotImplementedError

    def setup(self):
        return NotImplementedError

