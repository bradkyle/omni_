import asyncio_redis

# Store
# =====================================================================================================================>

class Store():
    def __init__(self,
                 host='127.0.0.1',
                 port=6379,
                 poolsize=10):
        self.host = host
        self.port = port
        self.poolsize = poolsize

    async def get(self, key):
        connection = await asyncio_redis.Pool.create(host=self.host, port=self.port, poolsize=self.poolsize)
        value = await connection.get(key)
        connection.close()
        return value

    async def set(self, key, value):
        connection = await asyncio_redis.Pool.create(host=self.host, port=self.port, poolsize=self.poolsize)
        await connection.set(key, value)
        connection.close()

    async def destroy(self, key):
        if type(key) == list:
            connection = await asyncio_redis.Pool.create(host=self.host, port=self.port, poolsize=self.poolsize)
            await connection.delete(key)
            connection.close()
        else:
            raise TypeError("Destroy key sould be a list type")

store = Store()

async def get(key):
    return await store.get(key)

async def set(key, value):
    return await store.set(key,value)

async def destroy(key):
    return await store.destroy(key)
