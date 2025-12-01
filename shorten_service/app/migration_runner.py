import os
from cassandra_connection import CassandraClient

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "url_shortener")

def run_migrations():
    session = CassandraClient.get_session()

    session.execute(f"""
        CREATE TABLE IF NOT EXISTS {KEYSPACE}.schema_migrations (
            version text PRIMARY KEY,
            applied_at timestamp
        );
    """)

    rows = session.execute(f"SELECT version FROM {KEYSPACE}.schema_migrations;")
    applied = {row.version for row in rows}

    migration_files = sorted(os.listdir(MIGRATIONS_DIR))

    for file in migration_files:
        version = file.split("_")[0]
        if version in applied:
            continue

        path = os.path.join(MIGRATIONS_DIR, file)
        with open(path, "r") as f:
            queries = f.read().split(";")

        for q in queries:
            q = q.strip()
            if q:
                session.execute(q)

        session.execute(
            f"INSERT INTO {KEYSPACE}.schema_migrations (version, applied_at) VALUES (%s, toTimestamp(now()));",
            (version,)
        )


if __name__ == "__main__":
    run_migrations()
