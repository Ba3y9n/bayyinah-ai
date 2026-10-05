import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import SessionLocal
from sqlalchemy import text

with SessionLocal() as db:
    res = db.execute(text("""
        SELECT conname, pg_get_constraintdef(c.oid)
        FROM pg_constraint c
        JOIN pg_namespace n ON n.oid = c.connamespace
        WHERE conrelid = 'sources'::regclass;
    """))
    for r in res.fetchall():
        print(f"{r[0]}: {r[1]}")
