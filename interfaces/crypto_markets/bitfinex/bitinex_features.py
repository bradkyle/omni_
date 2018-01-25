from omni.core import interface
from .bitinex_core import pub_service, priv_service

# Public
# -------------------------------------------------------------------------------------------------------------------->

@interface
async def get_symbols(input):
    endpoint = "/symbols"
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 5/min

@interface
async def get_ticker(input):
    endpoint = "/pubticker/" + str(input.symbol)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 30/min

@interface
async def get_stats(input):
    endpoint = "/stats/" + str(input.symbol)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 10/min

@interface
async def get_lendbook(input):
    endpoint = "/lendbook/" + str(input.currency)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 45/min

@interface
async def get_orderbook(input):
    endpoint = "/book/" + str(input.symbol)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 60/min

@interface
async def get_trades(input):
    endpoint = "/trades/" + str(input.symbol)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 45/min

@interface
async def get_lends(input):
    endpoint = "/lends/" + str(input.currency)
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 60/min

@interface
async def get_symbols_details(input):
    endpoint = "/symbols_details"
    return await pub_service.invoke(endpoint=endpoint) #todo rate_limit = 5/min

# Private
# -------------------------------------------------------------------------------------------------------------------->

@interface
async def get_account_info(input):
    endpoint = "/account_infos"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_account_fees(input):
    endpoint = "/account_fees"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_summary(input):
    endpoint = "/summary"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_key_info(input):
    endpoint = "/key_info"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_margin_infos(input):
    endpoint = "/margin_infos"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_balances(input):
    endpoint = "/balances"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce()
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_order_status(input):
    endpoint = "/order/status"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'id':input.order_id,
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_active_orders(input):
    endpoint = "/orders"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_order_history(input):
    endpoint = "/orders/hist"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_positions(input):
    endpoint = "/positions"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_balance_history(input):
    endpoint = "/history"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'currency': input.currency,
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_history_movements(input):
    endpoint = "/history/movements"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'currency': input.currency,
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_mytrades(input):
    endpoint = "/mytrades"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'currency': input.currency,
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_offer_status(input):
    endpoint = "/offer/status"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'offer_id': input.offer_id,
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_active_credits(input):
    endpoint = "/credits"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_active_offers(input):
    endpoint = "/offers"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_offers_history(input):
    endpoint = "/offers/hist"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_past_funding_trades(input):
    endpoint = "/mytrades_funding"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
        'symbol': input.symbol
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_taken_funds(input):
    endpoint = "/taken_funds"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_unused_taken_funds(input):
    endpoint = "/unused_taken_funds"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def get_total_taken_funds(input):
    endpoint = "/total_taken_funds"

    payload = {
        "request": priv_service.API_VERSION + endpoint,
        'nonce': await priv_service.get_nonce(),
    }

    return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)











































