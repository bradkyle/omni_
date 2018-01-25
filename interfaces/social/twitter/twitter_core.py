import base64
from omni.service import Service

class TwitterService(Service):
    def __init__(self):
        self.BASE_URI = "https://api.twitter.com/1.1"
        self.AUTH_URI = '{}oauth2/token'.format(self.BASE_URI)
        self.scope = "twitter"


    # todo complete
    async def invoke(self, endpoint, payload=None, params=None, keys=None, cache_length=None, rate_limit=None):
        url = self.BASE_URI + endpoint

        client_key = keys["consumer_key"]
        client_secret = keys["consumer_secret"]

        key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')

        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        auth_data = {
            'grant_type': 'client_credentials'
        }

        # todo make interface and give inherent rate limit
        auth_resp = await self._invoke("POST", self.AUTH_URI, headers=auth_headers, body=auth_data)

        auth_resp.json().keys()

        access_token = auth_resp.json()['access_token']

        search_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        return self._invoke("POST", self.AUTH_URI, headers=search_headers, params=payload)

service = TwitterService()

