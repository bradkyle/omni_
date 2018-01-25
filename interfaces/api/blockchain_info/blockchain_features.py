from omni.core import interface
from .blockchain_core import service

@interface
async def get_simple_data(input):
    return await service.invoke("GET", "/q/" + str(input.label))

@interface
async def get_chart(input):
    return await service.invoke("GET", "/charts/" + str(input.chart))

@interface
async def get_ticker(input):
    return await service.invoke("GET", "/ticker")

@interface
async def get_stats(input):
    return await service.invoke("GET", "/stats")

@interface
async def get_pools(input):
    return await service.invoke("GET", "/pools")

