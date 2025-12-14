# migration_runner.py
import os
from pathlib import Path
from typing import Iterable

def _split_statements(cql_text: str) -> Iterable[str]:
    # naive split by ';' and strip. Good for simple DDL migration files.
    for stmt in cql_text.split(';'):
        s = stmt.strip()
        if s:
            yield s

def run_migrations(session, migrations_dir: str):
    """
    session: cassandra session already connected to the target keyspace.
    migrations_dir: path to directory containing migration files named like '001_init.cql'
    """
    migrations_path = Path(migrations_dir)
    if not migrations_path.exists():
        print(f"[migrations] No migrations dir at {migrations_dir}, skipping.")
        return

    # Read applied versions
    try:
        rows = session.execute("SELECT version FROM schema_migrations;")
        applied = {row.version for row in rows}
    except Exception as e:
        # If schema_migrations is missing we should have created it in bootstrap before calling this.
        raise RuntimeError("Failed to read schema_migrations. Make sure bootstrap created it.") from e

    files = sorted(f for f in migrations_path.iterdir() if f.is_file() and f.name.endswith(".cql"))
    for f in files:
        version = f.name.split("_")[0]
        if version in applied:
            print(f"[migrations] Skipping applied migration {f.name}")
            continue

        print(f"[migrations] Applying {f.name} ...")
        text = f.read_text(encoding='utf-8')
        for stmt in _split_statements(text):
            try:
                session.execute(stmt)
            except Exception as e:
                raise RuntimeError(f"Failed to execute statement in {f.name}: {e}") from e

        # mark applied
        session.execute("INSERT INTO schema_migrations (version, applied_at) VALUES (%s, toTimestamp(now()))", (version,))
        print(f"[migrations] Applied {f.name}")
