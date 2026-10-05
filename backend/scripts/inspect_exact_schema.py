import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import SessionLocal
from sqlalchemy import text

tables_to_check = [
    "sources", "documents", "document_sections", "document_chunks",
    "verification_sessions", "claims", "evidence", "verification_results",
    "verification_evidence", "url_submissions", "media_assets", "media_artifacts",
    "ingestion_jobs", "source_versions", "chat_sessions", "chat_messages",
    "chat_evidence_bindings", "audit_logs"
]

with SessionLocal() as db:
    for t in tables_to_check:
        res = db.execute(text(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_schema='public' AND table_name=:tbl ORDER BY ordinal_position;"
        ), {"tbl": t})
        cols = res.fetchall()
        if cols:
            col_names = [f"{c[0]} ({c[1]})" for c in cols]
            print(f"Table {t} ({len(cols)} cols):\n  " + ", ".join(col_names))
        else:
            print(f"Table {t}: *** MISSING ***")
