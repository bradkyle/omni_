from .coinmarketcap_core import service
from omni.core import interface

#
@interface
async def get_all_tickers(input):
    params = {}
    params["limit"] = 3
    params["limit"] = input.start
    return await service.invoke("GET", endpoint='ticker/',rate_limit=input.rate_limit)

@interface
async def get_ticker(input):
    return await service.invoke("GET", endpoint='ticker/' + str(input.currency) + "/",rate_limit=input.rate_limit)

@interface
async def get_stats(input):
    return await service.invoke("GET", endpoint='global/',rate_limit=input.rate_limit)