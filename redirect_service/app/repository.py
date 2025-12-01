from .cassandra_connection import CassandraClient
from .models import ShortURL

class URLRepository:
    
    @staticmethod
    def get(short_code:str):
        session = CassandraClient.get_session()
        query = """
            SELECT short_code, long_url,created_at
            FROM url_map
            WHERE short_code = %s;
        """
        row = session.execute(query,(short_code,)).one()

        if not row:
            return None

        return ShortURL(
            short_code=row.short_code,
            long_url=row.long_url,
            created_at=row.created_at
        )