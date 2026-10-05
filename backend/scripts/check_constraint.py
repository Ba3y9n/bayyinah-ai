import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.database import SessionLocal
from sqlalchemy import text

with SessionLocal() as db:
    r = db.execute(text("""
        SELECT conname, pg_get_constraintdef(oid)
        FROM pg_constraint
        WHERE conrelid = 'documents'::regclass AND conname = 'documents_category_check';
    """)).fetchone()
    print("Constraint:", r)
