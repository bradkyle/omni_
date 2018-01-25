import base64
import hashlib
import hmac
import json
from omni.service import Service
from omni.interfaces.crypto_markets.market_core import MarketService
# todo handle errors particularly maintenence, i.e. if error deactivate all gemini affordances

class PublicGeminiService(MarketService, Service):
    def __init__(self):
        MarketService.__init__(self)
        self.API_VERSION = '/v1'
        self.BASE_URI = "https://api.sandbox.gemini.com" + self.API_VERSION
        self.scope = "gemini"

    async def invoke(self, endpoint, method=None, payload=None, params=None, keys=None, cache_length=None, rate_limit=None):
        url = self.BASE_URI + endpoint
        return await self._invoke("GET", url=url, payload=payload)

pub_service = PublicGeminiService()


class PrivateGeminiService(MarketService, Service):
    def __init__(self):
        MarketService.__init__(self)
        self.API_VERSION = '/v1'
        self.BASE_URI = "https://api.sandbox.gemini.com" + self.API_VERSION
        self.scope = "gemini"
        self.rate_limit = 600

    async def invoke(self, endpoint, method=None, payload=None, params=None, keys=None, cache_length=None, rate_limit=None):
        url = self.BASE_URI + endpoint

        content = payload

        cache_key = await self.gen_cache_key(keys['public'], url)

        # base64 encode the payload
        payload = str.encode(json.dumps(payload))
        b64 = base64.b64encode(payload)

        # sign the requests
        signature = hmac.new(str.encode(keys['private']), b64, hashlib.sha384).hexdigest()

        headers = {
            'Content-Type': 'text/plain',
            'X-GEMINI-APIKEY': keys['public'],
            'X-GEMINI-PAYLOAD': b64.decode('utf8'),
            'X-GEMINI-SIGNATURE': signature
        }

        # todo remove content from request

        return await self._invoke("POST", url=url, headers=headers, payload=content, cache_key=cache_key)


priv_service = PrivateGeminiService()