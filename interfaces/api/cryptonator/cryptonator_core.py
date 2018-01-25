from omni.service import Service

class Cryptonator(Service):
    def __init__(self):
        self.BASE_URI = 'https://api.cryptonator.com/api/'
        self.rate_limit = 2


service = Cryptonator()