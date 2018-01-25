from omni.service import Service


class MinCryptoCompareService(Service):
    def __init__(self):
        Service.__init__(self)
        self.BASE_URI = 'https://min-api.cryptocompare.com/data/'
        self.rate_limit = 0.01

service = MinCryptoCompareService()