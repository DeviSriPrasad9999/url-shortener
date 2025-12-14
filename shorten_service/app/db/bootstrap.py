# bootstrap.py
import os
import time
import socket
import uuid
import sys
from .cassandra_connection import CassandraClient
from .migration_runner import run_migrations  # this will accept a session
from pathlib import Path

KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "url_shortener")
MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"

MAX_CLUSTER_RETRIES = int(os.getenv("CASSANDRA_BOOTSTRAP_MAX_RETRIES", "30"))
RETRY_DELAY = float(os.getenv("CASSANDRA_BOOTSTRAP_RETRY_DELAY", "2"))

LOCK_TABLE = "schema_migration_lock"
MIGRATIONS_TABLE = "schema_migrations"
LOCK_KEY = "migration_lock"  # single-row lock

def wait_for_cluster_and_get_session():
    """Wait until cluster accepts connections and return a cluster-level session."""
    cluster = CassandraClient.get_cluster()
    last_exc = None
    for attempt in range(1, MAX_CLUSTER_RETRIES + 1):
        try:
            print(f"[bootstrap] Attempting cluster connect (attempt {attempt}/{MAX_CLUSTER_RETRIES})...")
            session = cluster.connect()  # cluster-level session
            print("[bootstrap] Cluster connection OK.")
            return session
        except Exception as e:
            last_exc = e
            print(f"[bootstrap] Cluster connect failed (attempt {attempt}): {e}")
            time.sleep(RETRY_DELAY)
    print("[bootstrap] Cluster never became available, exiting.")
    raise last_exc or RuntimeError("unable to connect to cassandra cluster")

def ensure_keyspace(cluster_session):
    """Idempotent keyspace creation (runs on cluster-level session)."""
    print(f"[bootstrap] Ensuring keyspace `{KEYSPACE}` exists...")
    cluster_session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
        WITH REPLICATION = {{
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }};
    """)
    # small pause so metadata refreshes
    time.sleep(1)
    print(f"[bootstrap] Keyspace `{KEYSPACE}` ensured.")

def ensure_migration_tables(keyspace_session):
    """Create schema_migrations and lock table if missing (idempotent)."""
    print("[bootstrap] Ensuring migrations metadata tables exist...")
    keyspace_session.execute(f"""
        CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
            version text PRIMARY KEY,
            applied_at timestamp
        );
    """)
    keyspace_session.execute(f"""
        CREATE TABLE IF NOT EXISTS {LOCK_TABLE} (
            id text PRIMARY KEY,
            owner text,
            locked_at timestamp
        );
    """)
    print("[bootstrap] Migration metadata tables ensured.")

def acquire_migration_lock(session, owner_id, timeout_seconds=60):
    """
    Acquire a distributed lock using a lightweight transaction (LWT).
    Returns True if lock acquired, False otherwise.
    """
    print(f"[bootstrap] Attempting to acquire migration lock as '{owner_id}' ...")
    query = f"INSERT INTO {LOCK_TABLE} (id, owner, locked_at) VALUES (%s, %s, toTimestamp(now())) IF NOT EXISTS"
    start = time.time()
    while True:
        try:
            res = session.execute(query, (LOCK_KEY, owner_id))
            applied = getattr(res, 'one', None)
            # cassandra-driver: res.one() returns Row. For LWT results, check '[0].applied' style:
            row = res.one()
            if row and getattr(row, "applied", False):
                print("[bootstrap] Lock acquired.")
                return True
            else:
                # not applied - someone else holds it
                print("[bootstrap] Lock held by another instance, waiting...")
        except Exception as e:
            print(f"[bootstrap] Lock attempt error: {e}")

        if time.time() - start > timeout_seconds:
            print("[bootstrap] Timeout acquiring migration lock.")
            return False
        time.sleep(2)

def release_migration_lock(session, owner_id):
    """Release lock only if owned by us (best-effort)."""
    try:
        # Conditional delete to prevent deleting someone else's lock:
        # We will read owner and delete only if matches (there is an IF clause possibility but simpler read+delete)
        row = session.execute(f"SELECT owner FROM {LOCK_TABLE} WHERE id=%s", (LOCK_KEY,)).one()
        if row and row.owner == owner_id:
            session.execute(f"DELETE FROM {LOCK_TABLE} WHERE id=%s", (LOCK_KEY,))
            print("[bootstrap] Lock released.")
        else:
            print("[bootstrap] Lock not owned by this process (skipping release).")
    except Exception as e:
        print(f"[bootstrap] Failed to release lock (non-fatal): {e}")

def main():
    owner_id = f"{socket.gethostname()}-{uuid.uuid4().hex[:8]}"
    cluster_session = wait_for_cluster_and_get_session()
    ensure_keyspace(cluster_session)

    # connect to keyspace AFTER it exists
    print(f"[bootstrap] Connecting to keyspace `{KEYSPACE}`...")
    keyspace_session = CassandraClient.connect(KEYSPACE)

    ensure_migration_tables(keyspace_session)

    # Acquire lock (LWT-based). If not acquired, wait and retry; if can't after timeout, exit or continue
    got_lock = acquire_migration_lock(keyspace_session, owner_id, timeout_seconds=120)
    if not got_lock:
        print("[bootstrap] Could not acquire migration lock; another instance is migrating. Proceeding without applying migrations.")
        return

    try:
        # run migrations using the active keyspace session
        print("[bootstrap] Running migrations...")
        run_migrations(keyspace_session, migrations_dir=str(MIGRATIONS_DIR))
        print("[bootstrap] Migrations finished.")
    finally:
        # always attempt to release lock
        release_migration_lock(keyspace_session, owner_id)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[bootstrap] Fatal error: {e}")
        # Exit non-zero so Docker detects failure (container should restart if configured)
        sys.exit(1)
