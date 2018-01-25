from .cryptonator_core import service
from omni.core import interface

@interface
async def get_supported_currency_list(input):
    return await service.invoke("GET", endpoint='currencies')

@interface
async def get_simple_ticker(input):
    return await service.invoke("GET", endpoint='ticker/' + input.quantity_currency + "-" + input.quote_currency)

@interface
async def get_full_ticker(input):
    return await service.invoke("GET", endpoint='full/' + input.quantity_currency + "-" + input.quote_currency)