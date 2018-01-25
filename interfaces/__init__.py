from omni.core import register, TYPE

GEMINI_KEY_SETS = [
    {"private": "3go1mGK4QSJkpFMdxtadRM6e9NoM", "public": "FdAVXfnhsnGwiEOOlDJY"},  # smithmalcolm46@gmail.com
    {"private": "u8rGPS1AvbWNqreT2U9rT4xAPPk", "public": "QzeR2u1AZuf5S6lXWrfo"},  # bradkyleduncan@gmail.com
    {"private": "26NheKRMDt6q24NFUASYVDYE4KPw", "public": "meMqYdKRQsxZDjOU6MRn"},  # wilnatfor@gmail.com
]

# Core
#=====================================================================================================================>
#
# for key in ['bad_request_penalty', 'bad_connection_penalty', 'none_response_penalty', 'not_afforded_penalty', 'rate_limit_penalty'
#              'step_penalty', 'not_found_penalty', 'response_size_penalty', 'affordance_disabled_penalty', 'wait_penalty', 'rate_limit_proximity_penalty']:
#     register(TYPE.CONFIG, entry_point="omni.interfaces.core.core_config.penalty_max", config_name=config_name, max_penalty=100)
#     register(TYPE.TASK, entrypoint="", key=key)


# CoinMarketCap Rate Limit = 10 per minute, Cache Length = 5 minutes. (https://coinmarketcap.com/api/)
# =====================================================================================================================>

for start in [0,3,6,9,12,15,18,21,24,27,30]:
    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.coinmarketcap.coinmarketcap_features:get_all_tickers', start=start)

register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.coinmarketcap.coinmarketcap_features:get_stats')


# Cryptocompare = 6 per minute, 6000 per hour(https://min-api.cryptocompare.com/ )   (https://www.cryptocompare.com/api/)
# =====================================================================================================================>

# todo




# Cryptonator Updates every 30 seconds
# =====================================================================================================================>

# todo
#
# register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.cryptonator.cryptonator_features:get_simple_ticker')
#
# register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.cryptonator.cryptonator_features:get_full_ticker')


# Etherchain
# =====================================================================================================================>


# Etherscan
# =====================================================================================================================>


# Quandl
# =====================================================================================================================>


# Webhose
# =====================================================================================================================>


# Wikipedia
# =====================================================================================================================>


# Bitfinex
# =====================================================================================================================>


# Gemini
# =====================================================================================================================>

register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_symbols')

for pair in ["btcusd", "ethusd", "ethbtc"]:

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_ticker', symbol=pair)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_order_book_asks', symbol=pair)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_order_book_bids', symbol=pair)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_current_auction', symbol=pair)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_auction_history', symbol=pair)

for key_set in GEMINI_KEY_SETS:

    register(TYPE.TASK, entry_point='omni.interfaces.markets.gemini.gemini_tasks:profit_over_time', key_set=key_set, currencies=["BTC", "ETH", "USD"])

    register(TYPE.CLOSER, entry_point='omni.interfaces.markets.gemini.gemini_closers:cancel_all_orders', key_set=key_set)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_active_orders', key_set=key_set)

    # todo loop for cancel order and order status

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_affordances:cancel_session_orders', key_set=key_set)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_affordances:cancel_all_orders', key_set=key_set)

    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_balance', key_set=key_set)

    for pair in ["btcusd", "ethusd", "ethbtc"]:

        register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_trade_volume', symbol=pair, key_set=key_set)

        register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_past_trades', symbol=pair, key_set=key_set, limit_trades=10)

        for option in ["maker-or-cancel", "immediate-or-cancel", "auction-only", None]:
            for side in ["buy", "sell"]:
                register(TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_affordances:new_order', symbol=pair, key_set=key_set, options=option, side=side)

#Blockchain Rate Limit = 6 per minute (https://blockchain.info/q, https://blockchain.info/api/charts_api)
#=====================================================================================================================>

for label in ["getdifficulty","getblockcount","latesthash","bcperblock",
                      "totalbc", "probability", "hashestowin", "nextretarget", "avgtxsize",
                      "avgtxvalue", "interval", "eta", "avgtxnumber", "unconfirmedcount", "24hrprice"
                      "marketcap", "24hrtransactioncount", "24hrbtcsent", "hashrate", "rejected"
                      ]:
    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.blockchain_info.blockchain_features:get_simple_data', label=label, rate_limit=6)


for chart in ["total-bitcoins","market-price","market-cap","trade-volume",
                      "blocks-size", "avg-block-size", "n-orphaned-blocks", "n-transactions-per-block", "median-confirmation-time",
                      "bip-9-segwit", "bitcoin-unlimited-share", "nya-support", "hash-rate", "difficulty", "miners-revenue",
                      "transaction-fees", "transaction-fees-usd", "cost-per-transaction-percent", "cost-per-transaction", "n-unique-addresses",
                      "n-transactions", "n-transactions-total", "transactions-per-second", "mempool-count", "mempool-growth", "mempool-size",
                      "utxo-count", "n-transactions-excluding-chains-longer-than-100", "output-volume", "estimated-transaction-volume",
                      "estimated-transaction-volume-usd", "my-wallet-n-users"]:
    register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.blockchain_info.blockchain_features:get_chart', chart=chart, cache_length=84000, rate_limit=0.0006)

register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.blockchain_info.blockchain_features:get_ticker', cache_length=900)

register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.blockchain_info.blockchain_features:get_stats', cache_length=900)

register(TYPE.AFFORDANCE, entry_point='omni.interfaces.api.blockchain_info.blockchain_features:get_pools', cache_length=900)


# Bitstamp
# =====================================================================================================================>


# Bittrex
# =====================================================================================================================>


# Coinbase GDAX
# =====================================================================================================================>


# Coinone
# =====================================================================================================================>


# Kraken
# =====================================================================================================================>


# Poloniex
# =====================================================================================================================>


# Quione
# =====================================================================================================================>


# Twitter
# =====================================================================================================================>

for key_set in [
        {"consumer_key":"WM1MVD31TRGZBiNbXO54p4Sni", "consumer_secret":"SJzN8rhCSyyzxt55shwpPScX1aEdOWX63q8d8yKC9gNAESsCjO", "access_token":"367687040-UzRMSNmwLjgjDl3CwAS72UbyeSkDOmKTKzmWSK89", "access_secret":"TAAu1ScD4pscR8nHTp3UyXx2T6JyCqOy5vTmcIYMtuGga"},
        {"consumer_key":"qnv3th6JUVEvTDoSHl5YcoYLl", "consumer_secret":"whgIR7PGf4zmlnlBaTQCIVPAudVBk1Tej93N0xW0vIpavjpQ6W", "access_token":"863416332095823872-LywT0OQYLI9smMDVDlTG6S9ygj8TA2x", "access_secret":"t6lYoMidHEumwiypurUArSzMMrn3VNQDXRsfXIANzZBsV"},
        {"consumer_key":"ghlSi83iK8b6Gt5r40Y5PB3Lh", "consumer_secret":"kSJkkeB3ggT0oErZ7xPyLOBWOOQytgmJPXao9pfhEnLXWXfyfn", "access_token":"367687040-P0WS0qnFihACmKdJNHo4m2tVy6LbUakZsLD7mse1", "access_secret":"Z30IzyTEKo4Tedk4fTazhJsz4YihtqY7NkKwoPAHGARYv"},
        {"consumer_key":"OVxT26UmJtdMLlJFY0vNDchRG", "consumer_secret":"c6iGLYINqU93qehJ9v84M1hVNXtmQGxtz6Pjs7aLO9X2aQh8aR", "access_token":"860540303421448193-RkErbZqOLToJQtxwk6oV5UhMEb7C9Uq", "access_secret":"VdOlI89dDaLYhCGXYZycWDAuGbVnklCbXyejpiSkziObK"},
        {"consumer_key":"ONoSdnInA2MHk5swW1FiGHBNl", "consumer_secret":"5pEwoWz97OE8BVTogM1nxtHfdkSjPkZkzAektGt8QAHGojkNuo", "access_token":"804937531749974016-ChkHvQwqOtsX1pKPnQRa4MqdGngXMTA", "access_secret":"OG7dxmYBD63749upwQRvSeJlafyJP6gW7SRWpJdWpMpYb"},
        {"consumer_key":"kIFURn1JdN2k1w0WUgENYz8w1", "consumer_secret":"8djbRqNF9Pg7J7Ofjv2tdXbObEWazrr4xt8FxWKMiev8qwhexb", "access_token":"860540303421448193-XJt9pKmqUye0yPXkSlm49LEtFHQ7lQW", "access_secret":"EiiuRn97OKEt4KXW7SQfmXvVjkR1Ec3ZHmTi1luRIUmKI"},
        {"consumer_key":"Zv9zY9KWONeU3qKbShxq9Oat9", "consumer_secret":"Uotuon99K26RCxtUkgB7KIBMjIKLaEQ8CFoCikCkqmDAstJCBX", "access_token":"860540303421448193-IgRs21k3HerMXA7eU97S90BZ3C460kF", "access_secret":"ab1WSco1X6jzmhNRNAnD1ieF7wmYGAKwK3ZbixwgyjuON"},
        {"consumer_key":"SpPvOhlmtNM3vDzK67XxT6r4A", "consumer_secret":"QvkZjhp4YnmpnE2bZpvsHe0HYwbuNonMLgplgQKbV3NUOfaOHH", "access_token":"804937531749974016-BynNs2n2PaK2VTvg0YlK92aBcArd9dr", "access_secret":"wvQ6jiey1T6ORhIwHZm3rMJi5UdRQTQgijHtqRUy9Xn7L"},
        {"consumer_key":"gtyPPsUvl94WPsevhBMm1xGQ2", "consumer_secret":"lgVN2CFlsXdVthgt4ZdVv1ExQNwCX2zdqv2rWkZ7ccpjkbuVG5", "access_token":"863416332095823872-MyeGXCHVAWwgQG93rCtIKpxS7444bou", "access_secret":"cDr0TZ7dHzx0HVzCdpLfkivyRjl2dDvYjXHkaXOxa2vp6"},
        {"consumer_key":"Zv9zY9KWONeU3qKbShxq9Oat9", "consumer_secret":"Uotuon99K26RCxtUkgB7KIBMjIKLaEQ8CFoCikCkqmDAstJCBX", "access_token":"860540303421448193-IgRs21k3HerMXA7eU97S90BZ3C460kF", "access_secret":"ab1WSco1X6jzmhNRNAnD1ieF7wmYGAKwK3ZbixwgyjuON"},
]:
    for term in ["bitcoin", "btc", "ether", "ethereum", "eth", "crypto", "c"]:
        register(TYPE.AFFORDANCE, entry_point='omni.interfaces.social.twitter.twitter_features:search', key_set=key_set, term=term)

print("Initialized interface registry.")