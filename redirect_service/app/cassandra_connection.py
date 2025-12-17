# app/db/cassandra_connection.py
import os
from typing import Optional
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy

class CassandraClient:
    _cluster: Optional[Cluster] = None
    _keyspace_session = None

    @classmethod
    def get_cluster(cls) -> Cluster:
        if cls._cluster is not None:
            return cls._cluster

        host = os.getenv("CASSANDRA_HOSTS").split(",")
        port = int(os.getenv("CASSANDRA_PORT", 9042))
        user = os.getenv("CASSANDRA_USER")
        password = os.getenv("CASSANDRA_PASS")

        auth = PlainTextAuthProvider(username=user, password=password) if user and password else None

        cls._cluster = Cluster(
            contact_points=host,
            port=port,
            auth_provider=auth,
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=os.getenv("CASSANDRA_DC")),
            connect_timeout=20,
            control_connection_timeout=20
        )
        return cls._cluster

    @classmethod
    def connect(cls, keyspace: Optional[str] = None):
        cluster = cls.get_cluster()
        if keyspace:
            return cluster.connect(keyspace)
        return cluster.connect()

    @classmethod
    def get_keyspace_session(cls):
        if cls._keyspace_session is not None:
            return cls._keyspace_session

        keyspace = os.getenv("CASSANDRA_KEYSPACE")
        if not keyspace:
            raise RuntimeError("CASSANDRA_KEYSPACE not set")

        cluster = cls.get_cluster()
        cls._keyspace_session = cluster.connect(keyspace)
        return cls._keyspace_session
