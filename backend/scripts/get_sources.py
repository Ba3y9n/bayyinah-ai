import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.database import SessionLocal
from app.models.knowledge_models import TrustedSourceModel, DocumentModel

with SessionLocal() as db:
    sources = db.query(TrustedSourceModel).filter(TrustedSourceModel.scientific_status == 'APPROVED').all()
    for s in sources:
        docs = db.query(DocumentModel).filter(DocumentModel.source_id == s.id).all()
        print(f"Source: {s.id} | {s.name_ar} | URL: {s.url}")
        for d in docs:
            print(f"   -> Doc: {d.id} | {d.title_ar}")
