from omni.service import Service

class CoinMarketCapService(Service):
    def __init__(self):
        self.BASE_URI = 'https://api.coinmarketcap.com/v1/'
        self.rate_limit = 2
        self.convert_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                                   "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                                   "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]


service = CoinMarketCapService()