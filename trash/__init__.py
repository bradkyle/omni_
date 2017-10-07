from omni.interfaces.registration import register

crypto_currencies = [
    {}
]

# Crypto Exchanges
# --------------------------------------------------------------------------------------------------------------------->

register(
    enabled = False,
    id='Gemini-v0',
    entry_point='omni.interfaces.crypto_exchanges:GeminiInterface',
    kwargs={
        'sandbox':False,
    }
)

register(
    id='GeminiSandBox-v0',
    entry_point='omni.interfaces.crypto_exchanges:GeminiInterface',
    kwargs={
        'sandbox':True,
    }
)

# PyExchange
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='PyExchangeOne-v0',
    entry_point='omni.interfaces.pyexchange:PyExchangeOneInterface',
    kwargs={
        'url':"http://pyexchange:1000",
    }
)

register(
    id='PyExchangeTwo-v0',
    entry_point='omni.interfaces.pyexchange:PyExchangeTwoInterface',
    kwargs={
        'url':"http://pyexchange:2000",
    }
)

register(
    id='PyExchangeThree-v0',
    entry_point='omni.interfaces.pyexchange:PyExchangeThreeInterface',
    kwargs={
        'url':"http://pyexchange:3000",
    }
)

register(
    id='PyExchangeFour-v0',
    entry_point='omni.interfaces.pyexchange:PyExchangeFourInterface',
    kwargs={
        'url':"http://pyexchange:4000",
    }
)

register(
    id='PyExchangeFive-v0',
    entry_point='omni.interfaces.pyexchange:PyExchangeFiveInterface',
    kwargs={
        'url':"http://pyexchange:5000",
    }
)

# PyWallet
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='PyWalletOne-v0',
    entry_point='omni.envs.interfaces:PyWalletOneInterface',
    kwargs={
        'url':"http://pywallet:1000",
    }
)

register(
    id='PyWalletTwo-v0',
    entry_point='omni.envs.interfaces:PyWalletTwoInterface',
    kwargs={
        'url':"http://pywallet:2000",
    }
)

register(
    id='PyWalletThree-v0',
    entry_point='omni.envs.interfaces:PyWalletThreeInterface',
    kwargs={
        'url':"http://pywallet:2000",
    }
)

# Crawl
# --------------------------------------------------------------------------------------------------------------------->

sources = [
    {"BlockChainInfo", },
    {"Etherchain" },

]

# API / Web
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='Twitter-v0',
    entry_point='omni.envs.interfaces:TwitterInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='Quandl-v0',
    entry_point='omni.envs.interfaces:QuandlInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

#todo
register(
    id='Wikipedia-v0',
    entry_point='omni.envs.interfaces:WikipediaInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='CoinMarketCap-v0',
    entry_point='omni.envs.interfaces:CoinMarketCapInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='Cryptonator-v0',
    entry_point='omni.envs.interfaces:CryptonatorInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='BlockChainInfo-v0',
    entry_point='omni.envs.interfaces:BlockChainInfoInterface',
    cache = True,
)

#todo
register(
    id='Etherchain-v0',
    entry_point='omni.envs.interfaces:EtherchainInterface',
    cache = True,
)

#todo
register(
    id='ChainNem-v0',
    entry_point='omni.envs.interfaces:ChainNemInterface',
    cache = True,
)

#todo
register(
    id='CoinMetrics-v0',
    entry_point='omni.envs.interfaces:CoinMetricsInterface',
    cache = True,
)

#
register(
    id='OnChainFX-v0',
    entry_point='omni.envs.interfaces:OnChainFXInterface',
    cache = True,
)

register(
    id='BitInfoCharts-v0',
    entry_point='omni.envs.interfaces:BitInfoChartsInterface',
    cache = True,
)

register(
    id='TokenData-v0',
    entry_point='omni.envs.interfaces:TokenDataInterface',
    cache = True,
)

register(
    id='CoinDance-v0',
    entry_point='omni.envs.interfaces:CoinDanceInterface',
    cache = True,
)

register(
    id='CryptoCoinCharts-v0',
    entry_point='omni.envs.interfaces:CryptoCoinChartsInterface',
    cache = True,
)

register(
    id='CoinGecko-v0',
    entry_point='omni.envs.interfaces:CoinGeckoInterface',
    cache = True,
)

register(
    id='CryptoCompare-v0',
    entry_point='omni.envs.interfaces:CryptoCompareInterface',
    cache = True,
)

register(
    id='BletchleyIndexes-v0',
    entry_point='omni.envs.interfaces:BletchleyIndexesInterface',
    cache = True,
)

register(
    id='CNNMoney-v0',
    entry_point='omni.envs.interfaces:CNNMoneyInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='Google-v0',
    entry_point='omni.envs.interfaces:GoogleInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='WebHose-v0',
    entry_point='omni.envs.interfaces:WebHoseInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='Reddit-v0',
    entry_point='omni.envs.interfaces:RedditInterface',
    kwargs = {
        "terms": {crypto_currencies}
    },
    cache = True,
)

register(
    id='USFederalReserve-v0',
    entry_point='omni.envs.interfaces:USFederalReserveInterface',
    kwargs = {
        "terms": {""}
    },
    cache = True,
)

register(
    id='USTreasury-v0',
    entry_point='omni.envs.interfaces:USTreasuryInterface',
    kwargs = {
        "terms": {""}
    },
    cache = True,
)

register(
    id='USBLS-v0',
    entry_point='omni.envs.interfaces:USBLSInterface',
    kwargs = {
        "terms": {""}
    },
    cache = True,
)

register(
    id='UsGovData-v0',
    entry_point='omni.envs.interfaces:UsGovDataInterface',
    kwargs = {
        "terms": {""}
    },
    cache = True,
)

