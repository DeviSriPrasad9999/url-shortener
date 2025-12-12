import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST","redis")
REDIS_PORT = os.getenv("REDIS_PORT",6379)
REDIS_DB = os.getenv("REDIS_DB",0)
REDIS_DECODE = True

def make_redis_client() -> redis.Redis:
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=REDIS_DECODE)

redis_client = make_redis_client()