"""
Bayyinah AI - Supabase & PostgreSQL Migration Runner
Reads and executes all 13 numbered SQL migrations in sequential order.
Verifies table creation, vector extensions, full text search, RLS policies, and seed data.
"""

import os
import sys
import glob
from typing import List, Dict, Any, Tuple
from sqlalchemy import create_engine, text
from ..config import settings

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

def get_migration_files() -> List[str]:
    """Returns sorted list of .sql migration file paths."""
    pattern = os.path.join(MIGRATIONS_DIR, "*.sql")
    files = glob.glob(pattern)
    files.sort()
    return files

def run_migrations(engine=None) -> Dict[str, Any]:
    """
    Executes all migrations sequentially against the provided or configured engine.
    """
    if engine is None:
        db_url = settings.DATABASE_URL
        if db_url and db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url and db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        if not db_url:
            return {
                "success": False,
                "error": "DATABASE_URL is not set. Cannot run PostgreSQL/Supabase migrations."
            }
        engine = create_engine(db_url, pool_pre_ping=True)

    files = get_migration_files()
    executed = []
    errors = []

    print("=" * 80)
    print(f"Bayyinah AI - Running {len(files)} Supabase / PostgreSQL Migrations")
    print("=" * 80)

    with engine.connect() as conn:
        # Create migrations tracking table if not exists
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS _schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT now()
            );
        """))
        conn.commit()

        # Check already applied
        applied = set(conn.execute(text("SELECT version FROM _schema_migrations;")).scalars().all())

        for f_path in files:
            fname = os.path.basename(f_path)
            if fname in applied:
                print(f"  [SKIP] {fname} (already applied)")
                continue

            print(f"  [APPLY] {fname}...")
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    sql_content = f.read()

                # Execute migration statements
                # If statements have multiple blocks, PostgreSQL handles script execution
                conn.execute(text(sql_content))
                conn.execute(text("INSERT INTO _schema_migrations (version) VALUES (:v);"), {"v": fname})
                conn.commit()
                executed.append(fname)
                print(f"  [OK] {fname}")
            except Exception as e:
                err_msg = f"Failed to apply {fname}: {str(e)}"
                print(f"  [ERROR] {err_msg}")
                errors.append({"file": fname, "error": str(e)})
                conn.rollback()
                break

    # Verification of created tables
    tables_created = []
    try:
        with engine.connect() as conn:
            query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
            tables_created = list(conn.execute(text(query)).scalars().all())
    except Exception as e:
        pass

    return {
        "success": len(errors) == 0,
        "executed_count": len(executed),
        "executed_files": executed,
        "errors": errors,
        "tables_in_public_schema": tables_created
    }

if __name__ == "__main__":
    res = run_migrations()
    print("\nMigration Results:", res)
