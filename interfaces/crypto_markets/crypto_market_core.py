import json
import time
from omni.utils import is_json
from omni.store import get, set
from omni.interfaces.api.cryptonator.cryptonator_features import get_simple_ticker
from omni.core import Input

class MarketService():
    def __init__(self):
        self.prev_balances = {}
        self.scope = None

    async def get_nonce(self):
        return time.time() * 1000

    async def calc_val_cryptocompare(self):
        return NotImplemented

    async def calc_value(self, quote_currency_symbol, balance, balance_currency_symbol="usd"):
        input = Input()
        input.quote_currency = balance_currency_symbol
        input.quantity_currency = quote_currency_symbol

        response = await get_simple_ticker(input)
        response = json.loads(response)
        #print(response)
        if balance_currency_symbol == "usd":
            resp_conversion = response["ticker"]["price"]
            value = float(resp_conversion) * float(balance)
        else:
            raise NotImplementedError
        return value

    #todo implement exponential moving average on profit as well as rate limiting and cache

    async def profit_over_time(self, id, current_value):
        if id in self.prev_balances:
            prev_balance = self.prev_balances[id]
            profit = float(current_value) - float(prev_balance["value"])
            profit_time = profit / (time.time() - prev_balance["time"])
        else:
            profit_time = 0.0
        self.prev_balances[id] = {"value": current_value, "time": time.time()}
        return profit_time

    async def get_max_order_price(self):
        return 1000

    async def get_max_order_size(self):
        return 1000

    # todo make sure insertion is successful
    async def get_next_order_id(self):

        assert self.scope is not None

        store_id = "current_"+str(self.scope)+"_order_id"
        current_gemini_order_id = await get(store_id)
        if current_gemini_order_id is None:
            current_gemini_order_id = 1
            await set(store_id, str(current_gemini_order_id))
        else:
            current_gemini_order_id = int(current_gemini_order_id)
            current_gemini_order_id += 1
            await set(store_id, str(current_gemini_order_id))
        return current_gemini_order_id