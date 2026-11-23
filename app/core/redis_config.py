import redis.asyncio as redis

KEY = "CNTR"

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def counter() -> str | None | bytes:
    await r.setnx(KEY, 100000)

    await r.incr(KEY)

    return await r.get(KEY)
