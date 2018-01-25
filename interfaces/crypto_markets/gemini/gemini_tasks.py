import json

from omni.core import interface
from .gemini_core import priv_service as service

@interface
async def profit_over_time(input):
    endpoint = '/balances'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': int(await service.get_nonce()),
    }

    # todo make sure response is json before loading

    response = json.loads(await service.invoke(endpoint=endpoint, payload=payload, keys=input.key_set))

    print(response)

    profits = []

    for balance in response:
        if balance["currency"] in input.currencies:

            balance_id = balance["currency"] + balance["type"] + input.key_set["public"]
            if balance["currency"] != "USD":
                balance_value = await service.calc_value(balance["currency"].lower(), balance["available"])
                profits.append(await service.profit_over_time(balance_id, balance_value))
            else:
                balance_value = balance["available"]
                profits.append(await service.profit_over_time(balance_id, balance_value))



    return profits