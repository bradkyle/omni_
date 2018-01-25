from omni.service import Service

class QuandlService(Service):
    def __init__(self):
        self.BASE_URI = "https://www.quandl.com/api/v3/datasets/"
        self.rate_limit = 30

service = QuandlService()