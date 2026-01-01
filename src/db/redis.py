from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600  

redis: Redis | None = None  

async def init_redis() -> None:
    global redis
    redis = Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True
    )
    try:
        await redis.ping()
        print("Redis connected successfully.")
    except Exception as e:
        print("Redis connection failed:", e)
        raise

async def add_jti_to_blocklist(jti: str) -> None:
    if redis is None:
        raise RuntimeError("Redis is not initialized")
    await redis.set(name=jti, value="revoked", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    if redis is None:
        raise RuntimeError("Redis is not initialized")
    result = await redis.get(jti)
    return result is not None
