import time

# Cache
# =====================================================================================================================>

class CacheItem():
    def __init__(self, key, value, duration):
        self.key = key
        self.value = value
        self.duration = duration
        self.timestamp = time.time()

    @property
    def valid(self):
        if time.time() >= self.timestamp + self.duration:
            return False
        else:
            return True

# todo the fetch should be done before replacement so as not to be left with nill
# Cache
class Cache():
    def __init__(self, length, delta=None):
        self.length = length
        self.delta = delta
        self.cache = {}

    # Insert new items to cache
    async def insert(self, key, value, length):
        if key in self.cache:
            del self.cache[key]
            self.cache[key] = CacheItem(key, value, length)

    # Remove those invalid items
    async def remove(self, key):
        if key in self.cache:
            del self.cache[key]

    async def lookup(self, key):
        if key in self.cache:
            if self.cache[key].valid:
                return True
            else:
                return False
        else:
            return False

    async def fetch(self, key):
        if key in self.cache:
            return self.cache[key]

    async def flush(self):
        for key, value in self.cache.items():
            if not value.valid:
                del self.cache[key]
            else:
                return


cache = Cache(1e6)
