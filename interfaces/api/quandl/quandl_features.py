from .quandl_core import service
from omni.core import interface

@interface
async def search(input):
    """
    For a list of all databases on Quandl, do this:

    https://www.quandl.com/api/v3/databases
    For a list of datasets in a given database, do this:

    https://www.quandl.com/api/v3/databases/WIKI/codes.json
    """
    params = {}

    endpoint = str(input.term) + "/data.json"

    return await service.invoke("GET", endpoint=endpoint, params=params)
