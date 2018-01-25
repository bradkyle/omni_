from .cryptocompare_core import service
from omni.core import interface

@interface
async def get_price(input):
    params = {}

    params["fsym"] = input.fsym
    params["tsyms"] = input.tsyms

    return await service.invoke("GET", params=params, endpoint="price")

@interface
async def get_mining_contracts(input):
    return NotImplemented

@interface
async def get_mining_equipment(input):
    return NotImplemented

@interface
async def get_mining_contracts(input):
    return NotImplemented

@interface
async def get_top_exchanges(input):
    return NotImplemented

@interface
async def get_top_coins(input):
    return NotImplemented

@interface
async def get_top_pairs(input):
    return NotImplemented

@interface
async def get_current_trading_info(input):
    return NotImplemented

@interface
async def get_day_average_price(input):
    return NotImplemented

@interface
async def get_historical_eod_price(input):
    return NotImplemented

@interface
async def get_historical_data(input):
    return NotImplemented

@interface
async def get_top_exchanges(input):
    return NotImplemented

@interface
async def get_coin_list(input):
    return NotImplemented

@interface
async def get_coin_snapshot(input):
    return NotImplemented