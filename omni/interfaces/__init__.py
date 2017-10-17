from omni.interfaces.registration import register, task

task(entry_point='omni.interfaces.markets.base:step_loss', per_step = 0.00001)

for chart in ["total-bitcoins","market-price","market-cap","trade-volume",
                      "blocks-size", "avg-block-size", "n-orphaned-blocks", "n-transactions-per-block", "median-confirmation-time",
                      "bip-9-segwit", "bitcoin-unlimited-share", "nya-support", "hash-rate", "difficulty", "miners-revenue",
                      "transaction-fees", "transaction-fees-usd", "cost-per-transaction-percent", "cost-per-transaction", "n-unique-addresses",
                      "n-transactions", "n-transactions-total", "transactions-per-second", "mempool-count", "mempool-growth", "mempool-size",
                      "utxo-count", "n-transactions-excluding-chains-longer-than-100", "output-volume", "estimated-transaction-volume",
                      "estimated-transaction-volume-usd", "my-wallet-n-users"]:
    register(entry_point='omni.interfaces.web.blockchain:get_chart', chart=chart, cached=True, cache_length=84000)

# register(entry_point='omni.interfaces.web.blockchain:get_ticker')
#
# register(entry_point='omni.interfaces.web.blockchain:get_stats')
#
# register(entry_point='omni.interfaces.web.blockchain:get_pools')
#
# register(entry_point='omni.interfaces.markets.gemini:get_symbols')
#
# for pair in ["btcusd", "ethusd", "ethbtc"]:
#
#     register(entry_point='omni.interfaces.markets.gemini:get_ticker', symbol=pair)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_order_book', symbol=pair)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_current_auction', symbol=pair)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_auction_history', symbol=pair)
#
# for key_set in [
#     {"private": "3go1mGK4QSJkpFMdxtadRM6e9NoM", "public": "FdAVXfnhsnGwiEOOlDJY"},  # smithmalcolm46@gmail.com
#     {"private": "u8rGPS1AvbWNqreT2U9rT4xAPPk", "public": "QzeR2u1AZuf5S6lXWrfo"},  # bradkyleduncan@gmail.com
#     {"private": "26NheKRMDt6q24NFUASYVDYE4KPw", "public": "meMqYdKRQsxZDjOU6MRn"},  # wilnatfor@gmail.com
# ]:
#     task(entry_point='omni.interfaces.markets.gemini:profit_over_time', key_set=key_set, cache=True, cache_length=10)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_active_orders', key_set=key_set)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_order_status', key_set=key_set)
#
#     register(entry_point='omni.interfaces.markets.gemini:cancel_order', key_set=key_set)
#
#     register(entry_point='omni.interfaces.markets.gemini:cancel_session_orders', key_set=key_set)
#
#     register(entry_point='omni.interfaces.markets.gemini:cancel_all_orders', key_set=key_set)
#
#     register(entry_point='omni.interfaces.markets.gemini:get_balance', key_set=key_set)
#
#     for pair in ["btcusd", "ethusd", "ethbtc"]:
#
#         register(entry_point='omni.interfaces.markets.gemini:get_trade_volume', symbol=pair, key_set=key_set)
#
#         register(entry_point='omni.interfaces.markets.gemini:get_past_trades', symbol=pair, key_set=key_set)
#
#         for option in ["maker-or-cancel", "immediate-or-cancel", "auction-only"]:
#             for side in ["buy", "sell"]:
#                 register(entry_point='omni.interfaces.markets.gemini:new_order', symbol=pair, key_set=key_set, options=option, side=side)
#
# for key_set in [
#     {"private": "3go1mGK4QSJkpFMdxtadRM6e9NoM", "public": "FdAVXfnhsnGwiEOOlDJY"},  # smithmalcolm46@gmail.com
#     {"private": "u8rGPS1AvbWNqreT2U9rT4xAPPk", "public": "QzeR2u1AZuf5S6lXWrfo"},  # bradkyleduncan@gmail.com
#     {"private": "26NheKRMDt6q24NFUASYVDYE4KPw", "public": "meMqYdKRQsxZDjOU6MRn"},  # wilnatfor@gmail.com
# ]:
#     for term in ["bitcoin", "btc", "ether", "ethereum", "eth"]:
#         register(entry_point='omni.interfaces.twitter.twitter:search', key_set=key_set, term=term)
#
#
# for key_set in [
#     {"private": "3go1mGK4QSJkpFMdxtadRM6e9NoM", "public": "FdAVXfnhsnGwiEOOlDJY"},  # smithmalcolm46@gmail.com
# ]:
#     for term in ["FRED/GDP", "BNC3/GWA_BTC", "BNC3/GWA_LTC",
#                  "USTREASURY/REALLONGTERM", "USTREASURY/REALYIELD", "USTREASURY/BILLRATES", "USTREASURY/YIELD", "USTREASURY/LONGTERMRATES", "USTREASURY/HQMYC"
#                  "USTREASURY/MATDIS", "USTREASURY/AVMAT", "USTREASURY/TNMBOR", "USTREASURY/TMBOR", "USTREASURY/MKTDM", "USTREASURY/BRDNM"]:
#         register(entry_point='omni.interfaces.quandl.quandl:search', key_set=key_set, term=term)
#
#
# for chart in ["tx","address","etherprice","marketcap",
#               "ethersupplygrowth", "hashrate", "difficulty", "pendingtx", "blocks",
#               "uncles", "blocksize", "blocktime", "gasprice", "gaslimit", "gasused",
#               "ethersupply", "chaindatasizefull", "chaindatasizefast", "ens-register"]:
#     register(entry_point='omni.interfaces.web.etherscan:get_chart', chart=chart)
#
#
# for convert in ["AUD", "BRL", "CAD", "CHF", "CNY", "EUR", "GBP", "HKD", "IDR", "INR", "JPY", "KRW", "MXN", "RUB"]:
#     register(entry_point='omni.interfaces.web.coinmarketcap:get_all_tickers', cache=True, cache_length=300, convert=convert)
#
# for convert in ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR",
#                 "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]:
#     register(entry_point='omni.interfaces.web.coinmarketcap:get_stats', convert=convert)
#

