from datetime import datetime
from .cassandra_connection import CassandraClient
from .models import ShortUrl

class URLRepository:

    @staticmethod
    def save(short_code:str, long_url:str):
        session = CassandraClient.get_session()

        query = """
            INSERT INTO url_map (short_code,long_url, created_at)
            VALUES (%s,%s,toTimestamp(now()));
        """
        session.execute(query,(short_code,long_url))

    @staticmethod
    def get(short_code:str):
        session = CassandraClient.get_session()

        query = """
            SELECT short_code, long_url,created_at
            FROM url_map
            WHERE short_code=%s;
        """
        row = session.execute(query,(short_code)).one()

        if not row:
            return None

        return ShortUrl(
            short_code=row.short_code,
            long_url=row.long_url,
            created_at=row.created_at
        )