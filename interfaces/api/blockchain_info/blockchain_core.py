from omni.service import Service

class BlockchainService(Service):
    def __init__(self):
        self.BASE_URI = "https://api.blockchain.info"

service = BlockchainService()