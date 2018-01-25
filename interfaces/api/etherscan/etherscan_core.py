from omni.service import Service

class EtherscanService(Service):
    def __init__(self):
        self.BASE_URI = "https://etherscan.io/"


service = EtherscanService()