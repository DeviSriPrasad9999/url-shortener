from datetime import datetime
from .db.cassandra_connection import CassandraClient
from .models import ShortURL
from .redis_client import redis_client

CACHE_PREFIX = "url:"
CACHE_TTL_SECONDS = 60 * 60 * 24  # 24 hours
NEGATIVE_CACHE_TTL = 60  # 1 minute

class URLRepository:

    @staticmethod
    def _cache_key(code: str) -> str:
        return f"{CACHE_PREFIX}{code}"

    @staticmethod
    def save(short_code:str, long_url:str):
        session = CassandraClient.get_keyspace_session()
        key = URLRepository._cache_key(short_code)
        query = """
            INSERT INTO url_map (short_code,long_url, created_at)
            VALUES (%s,%s,toTimestamp(now()));
        """
        session.execute(query,(short_code,long_url))
        redis_client.set(key,long_url,ex=CACHE_TTL_SECONDS)