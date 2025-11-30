import os
import time
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra import ConsistencyLevel

class CassandraClient:
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is None:
            hosts = os.getenv("CASSANDRA_HOST", "cassandra").split(",")
            port = int(os.getenv("CASSANDRA_PORT", 9042))
            keyspace = os.getenv("CASSANDRA_KEYSPACE", "url_shortener")
            max_retries = int(os.getenv("CASSANDRA_MAX_RETRIES", "30"))
            retry_delay = int(os.getenv("CASSANDRA_RETRY_DELAY", "2"))

            profile = ExecutionProfile(
                load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
                consistency_level=ConsistencyLevel.LOCAL_ONE,
                request_timeout=30
            )

            username = os.getenv("CASSANDRA_USER")
            password = os.getenv("CASSANDRA_PASS")
            
            for attempt in range(1, max_retries + 1):
                try:
                    if username and password:
                        auth = PlainTextAuthProvider(username=username, password=password)
                        cluster = Cluster(
                            contact_points=hosts,
                            port=port,
                            auth_provider=auth,
                            execution_profiles={EXEC_PROFILE_DEFAULT: profile},
                            connect_timeout=30,
                            control_connection_timeout=30
                        )
                    else:
                        cluster = Cluster(
                            contact_points=hosts,
                            port=port,
                            execution_profiles={EXEC_PROFILE_DEFAULT: profile},
                            connect_timeout=30,
                            control_connection_timeout=30
                        )

                    session = cluster.connect()
                    session.execute(f"""
                        CREATE KEYSPACE IF NOT EXISTS {keyspace}
                        WITH REPLICATION = {{
                            'class': 'SimpleStrategy',
                            'replication_factor': 1
                        }};
                    """)
                    cls._session = cluster.connect(keyspace)
                    return cls._session
                    
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(retry_delay * attempt)
                    else:
                        raise

        return cls._session
