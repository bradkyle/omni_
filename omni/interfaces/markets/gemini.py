from omni.interfaces.util import invoke

""" Client for the Gemini Exchange REST API.

   Full API docs are here: https://docs.gemini.com
   """
import base64
import hashlib
import hmac
import json
import time

import requests

API_VERSION = '/v1'

gemini_pairs = ["btcusd", "ethusd", "ethbtc"]
gemini_assets = ["btc", "usd", "eth"]
sides = ["buy", "sell"]
gemini_options = ["maker-or-cancel", "immediate-or-cancel", "auction-only"]
side = "buy"
pair = "btcusd"
asset = "btc"
option = "maker-or-cancel"
keys = [
    {"private": "3go1mGK4QSJkpFMdxtadRM6e9NoM", "public": "FdAVXfnhsnGwiEOOlDJY"},  # smithmalcolm46@gmail.com
    {"private": "u8rGPS1AvbWNqreT2U9rT4xAPPk", "public": "QzeR2u1AZuf5S6lXWrfo"},  # bradkyleduncan@gmail.com
    {"private": "26NheKRMDt6q24NFUASYVDYE4KPw", "public": "meMqYdKRQsxZDjOU6MRn"},  # wilnatfor@gmail.com
]

key_set = {"private": "26NheKRMDt6q24NFUASYVDYE4KPw", "public": "meMqYdKRQsxZDjOU6MRn"}

BASE_URI = "https://api.sandbox.gemini.com" + API_VERSION


# Private API methods
# -------------------
def _get_order_count():
    return 1

def _get_next_order_id():
    return 1

def _get_nonce():
    return time.time() * 1000

def _invoke_api(endpoint, payload, params=None, pub=True, keys=None):
    """ Sends the request to the Gemini Exchange API.

        Args:
            endpoint (str):   URL the call will go to
            payload (dict):   Headers containing the request specifics
            params (dict, optional):    A dict containing URL parameters (for public API calls)
            pub(bool, optional):    Boolean value identifying a Public API call (True) or Private API call (False)
    """

    url = BASE_URI + endpoint


    if pub == False:
        if keys is None:
            raise Exception

        # base64 encode the payload
        payload = str.encode(json.dumps(payload))
        b64 = base64.b64encode(payload)

        # sign the requests
        signature = hmac.new(str.encode(keys['private']), b64, hashlib.sha384).hexdigest()

        headers = {
            'Content-Type': 'text/plain',
            'X-GEMINI-APIKEY': keys['public'],
            'X-GEMINI-PAYLOAD': b64,
            'X-GEMINI-SIGNATURE': signature
        }

        # build a request object in case there's an error so we can echo it
        request = {'payload': payload, 'headers': headers, 'url': url}

        return invoke("POST", url=url, headers=headers, request=request)
    else:
        request = {'payload': payload, 'url': url}
        return invoke("GET", url=url, params=params, request=request)




# Public API methods
# ------------------
# State
def get_symbols():
    """ https://docs.gemini.com/rest-api/#symbols """
    endpoint = '/symbols'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, pub=True)


def get_ticker(symbol):
    """ https://docs.gemini.com/rest-api/#ticker """
    endpoint = '/pubticker/' + symbol

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, pub=True)


def get_order_book(symbol):
    """ https://docs.gemini.com/rest-api/#current-order-book """
    endpoint = '/book/' + symbol

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, pub=True)


def get_trade_history(symbol, since=None, limit_trades=None, include_breaks=None):


    # todo convert integer repr [0.1, 0.666, 0.5454] into since, limit_trades, include_breaks

    """ https://docs.gemini.com/rest-api/#trade-history """

    # build URL parameters
    params = {}
    if since:
        params['since'] = since

    if limit_trades:
        params['limit_trades'] = limit_trades

    if include_breaks:
        params['include_breaks'] = include_breaks

    endpoint = '/trades/' + symbol

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, params, pub=True)



def get_current_auction(symbol):
    """ https://docs.gemini.com/rest-api/#current-aucion """
    endpoint = '/auction/' + symbol

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, pub=True)



def get_auction_history(symbol, since=None, limit_auction_results=None, include_indicative=None):

    # todo convert integer repr [0.1, 0.666, 0.5454] into since, limit_auction_results, include_indicative

    """ https://docs.gemini.com/rest-api/#auction-history """

    # build URL parameters
    params = {}
    if since:
        params['since'] = since

    if limit_auction_results:
        params['limit_auction_results'] = limit_auction_results

    if include_indicative:
        params['include_indicative'] = include_indicative

    endpoint = '/auction/' + symbol + '/history'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, params, pub=True)



# Order Status API
# https://docs.gemini.com/rest-api/#order-status
# ----------------------------------------------
# State
def get_active_orders(key_set):
    """ https://docs.gemini.com/rest-api/#get-active-orders """
    endpoint = '/orders'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)



def get_order_status(key_set, order_id):

    # todo convert integer repr [0.5454] to order_id

    """ https://docs.gemini.com/rest-api/#order-status """
    endpoint = '/order/status'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce(),
        'order_id': order_id
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)



def get_trade_volume(key_set):
    """ https://docs.gemini.com/rest-api/#get-trade-volume """
    endpoint = '/tradevolume'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)



def get_past_trades(key_set, symbol, limit_trades=50, timestamp=None):

    # todo convert integer repr [0.5454, 0.65656 ...] to limit_trades (max=500), and timestamp

    """ https://docs.gemini.com/rest-api/#get-past-trades """
    endpoint = '/mytrades'

    payload = {
        'request': API_VERSION + endpoint,
        'symbol': symbol,
        'nonce': _get_nonce(),
        'limit_trades': limit_trades,
        'timestamp': timestamp
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)



# Order Placement API
# https://docs.gemini.com/rest-api/#new-order
# -------------------------------------------
# Action
def new_order(key_set, client_order_id, symbol, amount, price, side, options=None):

    # todo Automatic order id maker
    # todo convert integer repr [0.5454, 0.65656 ...] to amount and price

    """ https://docs.gemini.com/rest-api/#new-order """
    endpoint = '/order/new'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce(),
        'client_order_id': client_order_id,
        'symbol': symbol,
        'amount': amount,
        'price': price,
        'side': side,
        'type': 'exchange limit',
        'options': options
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)



def cancel_order(key_set, order_id):

    # todo convert integer repr [0.5454 ...] to order_id

    """ https://docs.gemini.com/rest-api/#cancel-order """
    endpoint = '/order/cancel'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce(),
        'order_id': order_id
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)




def cancel_session_orders(key_set):
    """ https://docs.gemini.com/rest-api/#cancel-all-session-orders """
    endpoint = '/order/cancel/session'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)




def cancel_all_orders(key_set):
    """ https://docs.gemini.com/rest-api/#cancel-all-active-orders """
    endpoint = '/order/cancel/all'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)




# Fund Management API's
# https://docs.gemini.com/rest-api/#get-available-balances
# --------------------------------------------------------
def get_balance(key_set):
    """ https://docs.gemini.com/rest-api/#get-available-balances """
    endpoint = '/balances'

    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    return _invoke_api(endpoint, payload, keys=key_set, pub=False)




# Tasks
# =====================================================================================================================>

# todo must cache
def profit_over_time(keys):
    session = requests.Session()

    endpoint ='/balances'
    url = BASE_URI + endpoint
    payload = {
        'request': API_VERSION + endpoint,
        'nonce': _get_nonce()
    }

    if keys is None:
        raise Exception

    # base64 encode the payload
    payload = str.encode(json.dumps(payload))
    b64 = base64.b64encode(payload)

    # sign the requests
    signature = hmac.new(str.encode(keys['private']), b64, hashlib.sha384).hexdigest()

    headers = {
        'Content-Type': 'text/plain',
        'X-GEMINI-APIKEY': keys['public'],
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature
    }

    session.post(url=url,headers=headers)





