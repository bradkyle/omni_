from .registration import register

# Crypto Exchanges
# --------------------------------------------------------------------------------------------------------------------->

register(
    enabled = False,
    id = 'Gemini-I0',
    entry_point='omni.interfaces.crypto_exchanges:GeminiInterface',
    kwargs={
        'sandbox':False,
    }
)

register(
    id = 'GeminiSandbox-v0',
    entry_point='omni.interfaces.crypto_exchanges:GeminiInterface',
    kwargs={
        'sandbox':True,
    }
)

register(
    id = 'Bitfinex-v0',
    entry_point='omni.interfaces.crypto_exchanges:BitfinexInterface',
)

register(
    id = 'Bitfinex-v0',
    entry_point='omni.interfaces.crypto_exchanges:BitfinexInterface',
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
    id='PyWalletOne',
    entry_point='omni.envs.interfaces:PyWalletOneInterface',
    kwargs={
        'url':"http://pywallet:1000",
    }
)

register(
    id='PyWalletTwo',
    entry_point='omni.envs.interfaces:PyWalletTwoInterface',
    kwargs={
        'url':"http://pywallet:2000",
    }
)

register(
    id='PyWalletThree',
    entry_point='omni.envs.interfaces:PyWalletThreeInterface',
    kwargs={
        'url':"http://pywallet:2000",
    }
)

# Twitter
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='Twitter-v0',
    entry_point='omni.interfaces.twitter:TwitterInterface',
    rate_limit= 1,
    cached = True,
    cache_length = 5,
)

# Google
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='GoogleTrends-v0',
    entry_point='omni.interfaces.google:GoogleTrendsInterface',
    cached = True,
    cache_length = 60,
)

register(
    id='GoogleFinance-v0',
    entry_point='omni.interfaces.google:GoogleFinanceInterface',
    cached = True,
    cache_length = 5,
)

# Webhose
# --------------------------------------------------------------------------------------------------------------------->

register(
    id='Webhose-v0',
    entry_point='omni.interfaces.google:GoogleFinanceInterface',
    rate_limit=0.02,
    cached = True,
    cache_length = 1200,
)