from .cassandra_connection import CassandraClient
from .models import ShortURL
from .redis_client import redis_client
from typing import Optional

CACHE_PREFIX = "url:"
CACHE_TTL_SECONDS = 60 * 60 * 24
NEGATIVE_CACHE_TTL = 60

class URLRepository:
    
    @staticmethod
    def _cache_key(code: str) -> str:
        return f"{CACHE_PREFIX}{code}"
    
    @staticmethod
    def get(short_code:str) -> Optional[ShortURL]:
        key = URLRepository._cache_key(short_code)
        try:
            cached = redis_client.get(key)
        except Exception as e:
            cached = None
        
        if cached is not None:
            if cached == "__NOT_FOUND__":
                return None
            return ShortURL(short_code=short_code, long_url=cached, created_at=None)
        
        session = CassandraClient.get_session()
        query = """
            SELECT short_code, long_url,created_at
            FROM url_map
            WHERE short_code = %s;
        """
        try:
            row = session.execute(query,(short_code,)).one()
        except Exception as e:
            return None
        
        if not row:
            try:
                redis_client.set(key,"__NOT_FOUND", ex=NEGATIVE_CACHE_TTL)
            except Exception:
                pass
            return None

        long_url = row.long_url
        try:
            redis_client.set(key,long_url,ex=CACHE_TTL_SECONDS)
        except Exception:
            pass

        return ShortURL(
            short_code=row.short_code,
            long_url=row.long_url,
            created_at=row.created_at
        )