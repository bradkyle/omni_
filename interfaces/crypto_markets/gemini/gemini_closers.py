from omni.core import interface
from .gemini_core import priv_service as service

@interface
async def cancel_session_orders(input):
    """ https://docs.gemini.com/rest-api/#cancel-all-session-orders """
    endpoint = '/order/cancel/session'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint, payload, keys=input.key_set)

@interface
async def cancel_all_orders(input):
    """ https://docs.gemini.com/rest-api/#cancel-all-active-orders """
    endpoint = '/order/cancel/all'

    payload = {
        'request': service.API_VERSION + endpoint,
        'nonce': await service.get_nonce()
    }

    return await service.invoke(endpoint, payload, keys=input.key_set)