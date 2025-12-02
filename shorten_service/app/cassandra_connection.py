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
        port = int(os.getenv("CASSANDRA_PORT"))
        keyspace = os.getenv("CASSANDRA_KEYSPACE")

        username = os.getenv("CASSANDRA_USER")
        password = os.getenv("CASSANDRA_PASS")

        auth = PlainTextAuthProvider(
            username=username,
            password=password
        )

        cluster = Cluster(
            contact_points=[host],
            port=port,
            auth_provider=auth
        )

        session = cluster.connect()

        # Now connect to the keyspace
        cls._session = cluster.connect(keyspace)
        return cls._session
