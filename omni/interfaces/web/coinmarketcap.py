import json
import requests
from omni.interfaces.util import invoke

BASE_URL = 'https://api.coinmarketcap.com/v1/'


def get_all_tickers(convert=None, limit=None):
    # todo convert integer repr [0.1] into limit

    """
    Returns a dict containing one/all the currencies
    Optional parameters:
    (int) limit - only returns the top limit results.
    (string) convert - return price, 24h volume, and market cap in terms of another currency. Valid values are:
    "AUD", "BRL", "CAD", "CHF", "CNY", "EUR", "GBP", "HKD", "IDR", "INR", "JPY", "KRW", "MXN", "RUB"
    """

    params = {}
    if convert:
        params['convert'] = convert

    if limit:
        params['limit'] = limit

    return invoke("GET", url=BASE_URL+'ticker/', params=params)

def get_ticker(currency="", convert=None, limit=None):
    """
    Returns a dict containing one/all the currencies
    Optional parameters:
    (int) limit - only returns the top limit results.
    (string) convert - return price, 24h volume, and market cap in terms of another currency. Valid values are:
    "AUD", "BRL", "CAD", "CHF", "CNY", "EUR", "GBP", "HKD", "IDR", "INR", "JPY", "KRW", "MXN", "RUB"
    """

    params = {}
    if convert:
        params['convert'] = convert

    if limit:
        params['limit'] = limit

    return invoke("GET", url=BASE_URL + 'ticker/' + currency, params=params)


def get_stats(convert = None):
    """
    Returns a dict containing cryptocurrency statistics.
    Optional parameters:
    (string) convert - return 24h volume, and market cap in terms of another currency. Valid values are:
    "AUD", "BRL", "CAD", "CHF", "CNY", "EUR", "GBP", "HKD", "IDR", "INR", "JPY", "KRW", "MXN", "RUB"
    """

    params = {}
    if convert:
        params['convert'] = convert

    return invoke("GET", url=BASE_URL + 'global/', params=params)