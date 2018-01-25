import json
from omni.utils import is_json
from .gemini_core import priv_service as service
from omni.core import interface, TYPE, register
from omni.penalty import BadResponsePenalty
from omni.utils import is_json

# Fund Management API's
# https://docs.gemini.com/rest-api/#get-available-balances
# --------------------------------------------------------

async def new_deposit_address(input):
    """ https://docs.gemini.com/rest-api/#new-deposit-address """
    endpoint = '/' + input.currency + '/newAddress'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'label': input.label
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)


async def withdraw_crypto(input):
    """ https://docs.gemini.com/rest-api/#withdraw-crypto-funds-to-whitelisted-address """
    endpoint = '/withdraw/' + input.currency

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'address': input.address,
        'amount': input.amount
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)


# Order Placement API
# https://docs.gemini.com/rest-api/#new-order
# -------------------------------------------

@interface
async def cancel_order(input):

    endpoint = '/order/cancel'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'order_id': input.order_id
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

@interface
async def cancel_session_orders(input):
    """ https://docs.gemini.com/rest-api/#cancel-all-session-orders """
    endpoint = '/order/cancel/session'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)

@interface
async def cancel_all_orders(input):
    """ https://docs.gemini.com/rest-api/#cancel-all-active-orders """
    endpoint = '/order/cancel/all'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)


@interface
async def new_order(input):

    client_order_id = str(await service.get_next_order_id())

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
    endpoint = '/order/new'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce(),
        'client_order_id': client_order_id,
        'symbol': input.symbol,
        'amount': amount,
        'price': price,
        'side': input.side,
        'type': 'exchange limit'
    }

    if input.options is not None and not "":
        payload['options'] = [input.options]

    response = await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set)
    if response is not None and is_json(response):
        loaded_response = json.loads(response)

        if "result" not in loaded_response:

            if type(loaded_response) == list:
                if "order_id" in loaded_response[0]:
                    new_order_id = loaded_response[0]["order_id"]
                else:
                    print("Encountered error in gemini new order list")
                    await BadResponsePenalty()  # todo change to penalise
                    return response
            else:
                if "order_id" in loaded_response:
                     new_order_id = loaded_response["order_id"]
                else:
                    print("Encountered error in gemini new order")
                    await BadResponsePenalty()  # todo change to penalise
                    return response



            register(type= TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_features:get_order_status', key_set=input.key_set, order_id=new_order_id) #todo rate limits
            register(type= TYPE.AFFORDANCE, entry_point='omni.interfaces.markets.gemini.gemini_affordances:cancel_order', key_set=input.key_set, order_id=new_order_id) #todo rate limits
        else:
            print("Encountered error in gemini new order")
            await BadResponsePenalty() #todo change to penalise
            return response
    else:
        print("Encountered error in gemini new order")
        await BadResponsePenalty() #todo change to penalise
        return response


