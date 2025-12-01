import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class CassandraClient:
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is not None:
            return cls._session

        host = os.getenv("CASSANDRA_HOST")
        port = int(os.getenv("CASSANDRA_PORT", 9042))
        keyspace = os.getenv("CASSANDRA_KEYSPACE")

        auth = PlainTextAuthProvider(
            username=os.getenv("CASSANDRA_USER"),
            password=os.getenv("CASSANDRA_PASS")
        )

        cluster = Cluster(contact_points=[host], port=port, auth_provider=auth)
        # Only connect
        cls._session = cluster.connect(keyspace)
        return cls._session
