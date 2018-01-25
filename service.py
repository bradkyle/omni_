import asyncio
import aiohttp
import json

# Service
# =====================================================================================================================>

class Request():
    def __init__(self):
        raise NotImplemented

class Response():
    def __init__(self):
        raise NotImplemented

class RequestHandler():
    def __init__(self):
        self.url_call_dict = {}

    async def inc(self, url):
        return NotImplemented

    async def proximity(self):
        return NotImplemented

    async def limit_rate(self):
        return NotImplemented

    async def get_wait_time(self):
        return NotImplemented

    async def get_current_request_rate(self):
        return NotImplemented



# todo allow for response checking before returning
class Service():

    def __new__(cls, *args, **kwargs):
        service = super(Service, cls).__new__(cls)
        service._disabled = False
        service._active = True
        service._spec = None

        service.base_rate_limit = 1 #per minute

        service.last_called = None #todo this should be moved onto the interfaces (or passed to by service) so as to be interface specific

        return service

    BASE_URI = None

    async def invoke(self, method, endpoint, headers=None, body=None, payload=None, params=None, rate_limit=None):
        if self.BASE_URI is not None:
            return await self._invoke(method, url=self.BASE_URI+endpoint, payload=payload, params=params)
        else:
            raise InvalidServiceError("BASE URI not set")

    async def _invoke(self, method, url, headers=None, body=None, params=None, payload=None, rate_limit=None, cache_length=None, cache_key=None):
        if rate_limit is None:
            rate_limit = self.base_rate_limit

        rate_limited = await self.limit_rate(rate_limit)

        if rate_limited:
            if cache_length is not None and await cache.lookup(cache_key):
                response, success = await self._cache(method, url, headers, body, params, payload)
            else:
                response = await self._fetch(method, url, headers, body, params, payload)
        else:
            if cache_length is not None:
                response, success = await self._cache(method, url, headers, body, params, payload)
            else:
                response = await self._fetch(method, url, headers, body, params, payload)

        return response

    async def _cache(self, method, url, headers=None, body=None, params=None, payload=None, cache_length=None, cache_key=None):
        async def _lookup_or_set(cache_key, cache_length):
            if await cache.lookup(cache_key):
                response = await cache.fetch(cache_key)
                return response
            else:
                response = await self._fetch(method, url, headers, body, params, payload)
                await cache.insert(cache_key, response, cache_length)
                return response

        if cache_key is not None:
            response = await _lookup_or_set(cache_key, cache_length)
            return response
        else:
            response = await _lookup_or_set(url, cache_length)
            return response, True

    async def _fetch(self, method, url, headers=None, body=None, params=None, payload=None):
        try:
            response = await self.__fetch(method,url,headers,params,body)
            if response is None:
                raise NoneResponseError("Empty response:" + str(response.status_code))
            await self.inc()
            return response

        except asyncio.TimeoutError as e:
            return await self.handle_error("Encountered asyncio.TimeoutError error: ", e)

        except HttpProcessingError as e:
            return await self.handle_error("Encountered HttpProcessingError error: ", e)

        except NoneResponseError as e:
            return await self.handle_error("Encountered NoneResponseError error: ", e)

        except aiohttp.ClientResponseError as e:
            return await self.handle_error("Encountered aiohttp.ClientResponseError error: ", e)

        except aiohttp.ClientConnectionError as e:
            return await self.handle_error("Encountered aiohttp.ClientConnectionError error: ", e)

    async def handle_error(self, pre_message, e):
        message =  pre_message + str(e)
        json_message = json.dumps({"error":message})
        print(message)
        #TODO PENALISE FOR ERROR
        return json_message

    async def __fetch(self, method, url, headers, params, body):
        async with aiohttp.ClientSession() as session:

            if method == "GET":
                async with session.get(url=url, headers=headers, params=params, json=body) as response:
                    return await response.text()

            if method == "POST":
                async with session.post(url=url, headers=headers, params=params, json=body) as response:
                    return await response.text()

    async def gen_cache_key(*args):
        return ''.join(map(str, args))

    async def inc(self):
        self.last_called = time.time()

    async def limit_rate(self, rate_limit):
        current_rate = await self.get_current_request_rate()
        if current_rate >= rate_limit:
            await omni.penalty.RateLimitPenalty() #todo change to penalize
            print("rate limiting ...")
            return True
        else:
            await omni.penalty.RateLimitProximityPenalty(rate_limit=rate_limit, current_rate=current_rate) #todo change to penalize
            return False

    # all call rates are referenced in minutes
    async def get_wait_time(self, rate_limit):
        if self.last_called is not None:
            return (self.last_called + (60/rate_limit)) - time.time()
        else:
            return 0

    # returns the number of requests
    # that are being made per minute
    async def get_current_request_rate(self):
        if self.last_called is not None:
            return 60/time.time() - self.last_called
        else:
            return 0

    async def switch(self, discrete, continuous):
        if discrete is not None:
            return discrete
        elif continuous is not None:
            return continuous

    async def wait_and_penalise(self):
        return NotImplemented
