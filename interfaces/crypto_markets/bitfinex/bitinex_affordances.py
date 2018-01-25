from omni.core import interface
from .bitinex_core import priv_service as service

@interface
async def deposit(input):
    endpoint = "/deposit/new"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        "method":input.method,
        "wallet_name": input.wallet_name,
        "renew": input.renew
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def withdraw(input):
    endpoint = "/withdraw"

    input_amount, input_amount_arg = None, None

    if hasattr(input, 'amount'):
        input_price = input.amount

    if hasattr(input, 'args'):
        input_amount_arg = input.args[0]

    if input_amount_arg is not None:
        arg_amount = abs(round(float(input_amount_arg) * float(await service.get_max_order_size()), 2))
    else:
        arg_amount = 0.0

    amount = await service.switch(input_amount, arg_amount)

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'withdraw_type': input.withdraw_type,
        "walletselected": input.walletselected,
        "amount":amount,
        "walletto": input.walletto,
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def transfer(input):
    endpoint = "/transfer"

    #todo standardize
    input_amount, input_amount_arg = None, None

    if hasattr(input, 'amount'):
        input_price = input.amount

    if hasattr(input, 'args'):
        input_amount_arg = input.args[0]

    if input_amount_arg is not None:
        arg_amount = abs(round(float(input_amount_arg) * float(await service.get_max_order_size()), 2))
    else:
        arg_amount = 0.0

    amount = await service.switch(input_amount, arg_amount)

    payload = {
        "request": service.API_VERSION + endpoint,
        "nonce": await service.get_nonce(),
        "amount": amount,
        "currency": input.currency,
        "walletfrom": input.walletfrom,
        "walletto": input.walletto,
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

# todo extend
@interface
async def new_order(input):
    endpoint = "/order/new"

    # todo standardize
    input_price, input_amount, input_price_arg, input_amount_arg = None, None, None, None

    if hasattr(input, 'price'):
        input_price = input.price

    if hasattr(input, 'amount'):
        input_amount = input.amount

    if hasattr(input, 'args'):
        input_price_arg = input.args[0]
        input_amount_arg = input.args[1]

    if input_price_arg is not None:
        arg_price = abs(round((float(input_price_arg) * float(await service.get_max_order_price())), 2))
    else:
        arg_price = 0.0

    if input_amount_arg is not None:
        arg_amount = abs(round(float(input_amount_arg) * float(await service.get_max_order_size()), 2))
    else:
        arg_amount = 0.0

    price = await service.switch(input_price, arg_price)
    amount = await service.switch(input_amount, arg_amount)

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'symbol': input.symbol,
        'amount': amount,
        'price': price,
        'exchange': 'bitfinex',
        'side': input.side,
        'type': input.type,
        'is_hidden': input.is_hidden,
        'is_postonly': input.is_postonly,
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)


@interface
async def cancel_order(input):
    endpoint = "/order/cancel"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'id': input.order_id,
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)


@interface
async def cancel_all_orders(input):
    endpoint = "/order/cancel/all"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def replace_order(input):
    endpoint = "/order/cancel/replace"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'id': input.order_id,
        'symbol': input.symbol
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def claim_position(input):
    endpoint = "/account_infos"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def new_offer(input):
    endpoint = "/account_infos"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def cancel_offer(input):
    endpoint = "/account_infos"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def close_margin_funding(input):
    endpoint = "/account_infos"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

@interface
async def basket_manage(input):
    endpoint = "/account_infos"

    payload = {
        "request": service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)

# @interface
# async def cancel_multiple_orders(input):
#     endpoint = "/account_infos"
#
#     payload = {
#         "request": service.API_VERSION + endpoint,
#         'nonce': await service.get_nonce()
#     }
#
#     return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)


# @interface
# async def multiple_new_orders(input):
#     endpoint = "/account_infos"
#
#     orders
#
#     payload = {
#         "request": service.API_VERSION + endpoint,
#         'nonce': await service.get_nonce()
#         'orders': orders
#     }
#
#     return await priv_service.invoke(endpoint=endpoint, payload=payload, keys=input.keys)