from omni.core import interface
from .twitter_core import service

@interface
async def search(input):

    search_params = {
        'q': input.q,
        'result_type': 'recent',
        'count': input.count
    }

    return service.invoke(endpoint="/search/tweets.json", payload=search_params, keys=input.keys)