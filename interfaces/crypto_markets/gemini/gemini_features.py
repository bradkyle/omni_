import json
from omni.utils import is_json
from omni.core import interface
from .gemini_core import pub_service, priv_service
from omni.penalty import BadResponsePenalty

@interface
async def get_symbols(input):
    """ https://docs.gemini.com/rest-api/#symbols """
    endpoint = '/symbols'

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    return await pub_service.invoke(endpoint=endpoint, payload=payload)

@interface
async def get_ticker(input):
    """ https://docs.gemini.com/rest-api/#ticker """
    endpoint = '/pubticker/' + input.symbol

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    return await pub_service.invoke(endpoint=endpoint, payload=payload)

@interface
async def get_order_book_asks(input):
    """ https://docs.gemini.com/rest-api/#current-order-book """
    endpoint = '/book/' + input.symbol

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    response = await pub_service.invoke(endpoint=endpoint, payload=payload)

    if is_json(response):
        dict_resp = json.loads(response)
        if "asks" in dict_resp:
            return json.dumps(dict_resp["asks"])
    else:
        return response



@interface
async def get_order_book_bids(input):
    """ https://docs.gemini.com/rest-api/#current-order-book """
    endpoint = '/book/' + input.symbol

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    response = await pub_service.invoke(endpoint=endpoint, payload=payload)

    if is_json(response):
        dict_resp = json.loads(response)
        if "bids" in dict_resp:
            return json.dumps(dict_resp["bids"])
    else:
        return response


@interface
async def get_trade_history(input):
    """ https://docs.gemini.com/rest-api/#current-order-book """

    endpoint = '/trades/' + input.symbol

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    return await pub_service.invoke(endpoint=endpoint, payload=payload)

@interface
async def get_current_auction(input):
    """ https://docs.gemini.com/rest-api/#current-aucion """
    endpoint = '/auction/' + input.symbol

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    return await pub_service.invoke(endpoint=endpoint, payload=payload)

@interface
async def get_auction_history(input):

    params = {}
    # params['since'] = since
    params['limit_auction_results'] = 5
    # params['include_indicative'] = include_indicative

    endpoint = '/auction/' + input.symbol + '/history'

    payload = {
        'request': pub_service.API_VERSION + endpoint,
        'nonce': await pub_service.get_nonce()
    }

    return await pub_service.invoke(endpoint=endpoint, payload=payload, params=params)

# Order Status API
# https://docs.gemini.com/rest-api/#order-status
# ----------------------------------------------
# State

@interface
async def get_active_orders(input):

    endpoint = '/orders'

    payload = {
        'request': priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

@interface
async def get_order_status(input):

    """ https://docs.gemini.com/rest-api/#order-status """
    endpoint = '/order/status'

    payload = {
        'request': priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'order_id': input.order_id
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

@interface
async def get_trade_volume(input):

    endpoint = '/tradevolume'

    payload = {
        'request': priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

@interface
async def get_past_trades(input):

    endpoint = '/mytrades'

    payload = {
        'request': priv_service.API_VERSION + endpoint,
        'symbol': input.symbol,
        'nonce': await priv_service.get_nonce(),
        'limit_trades': input.limit_trades
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

# Fund Management API's
# https://docs.gemini.com/rest-api/#get-available-balances
# --------------------------------------------------------

@interface
async def get_balance(input):
    """ https://docs.gemini.com/rest-api/#get-available-balances """
    endpoint = '/balances'

    payload = {
        'request': priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)