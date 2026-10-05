from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.knowledge_models import TrustedSourceModel, DocumentModel
from ..models.knowledge_schemas import (
    TrustedSourceResponse,
    TrustedSourceCreate,
    TrustedSourceUpdate,
    SourceHealthItem,
    DocumentResponse
)
from ..knowledge.source_registry import source_registry_service
from ..knowledge.source_health import source_health_service

router = APIRouter(prefix="/api/sources", tags=["Trusted Sources"])

@router.get("", response_model=List[TrustedSourceResponse])
def list_sources(
    category: Optional[str] = Query("all", description="Filter by category or 'all'"),
    db: Session = Depends(get_db)
):
    return source_registry_service.get_all_sources(db, category=category)

@router.get("/health", response_model=List[SourceHealthItem])
def get_all_sources_health(db: Session = Depends(get_db)):
    return source_health_service.check_all_sources_health(db)

@router.get("/category/{category}", response_model=List[TrustedSourceResponse])
def get_sources_by_category(category: str, db: Session = Depends(get_db)):
    return source_registry_service.get_all_sources(db, category=category)

@router.get("/{source_id}", response_model=TrustedSourceResponse)
def get_source_by_id(source_id: str, db: Session = Depends(get_db)):
    src = source_registry_service.get_source_by_id(db, source_id)
    if not src:
        raise HTTPException(status_code=404, detail="المصدر غير موجود في سجل المصادر المعتمدة")
    return src

@router.get("/{source_id}/health", response_model=SourceHealthItem)
def get_single_source_health(source_id: str, db: Session = Depends(get_db)):
    src = db.query(TrustedSourceModel).filter_by(id=source_id).first()
    if not src:
        raise HTTPException(status_code=404, detail="المصدر غير موجود")
    return source_health_service.check_source_health(src, db)

@router.get("/{source_id}/documents", response_model=List[DocumentResponse])
def get_source_documents(source_id: str, db: Session = Depends(get_db)):
    src = db.query(TrustedSourceModel).filter_by(id=source_id).first()
    if not src:
        raise HTTPException(status_code=404, detail="المصدر غير موجود")
    docs = db.query(DocumentModel).filter_by(source_id=source_id).all()
    res = []
    for d in docs:
        res.append(DocumentResponse(
            id=d.id,
            source_id=d.source_id,
            title_ar=d.title_ar,
            title_en=d.title_en,
            author=d.author,
            publisher=d.publisher,
            document_type=d.document_type,
            category=d.category, # type: ignore
            official_url=d.official_url,
            canonical_url=d.canonical_url,
            language=d.language,
            edition=d.edition,
            description=d.description,
            license_status=d.license_status, # type: ignore
            ingestion_status=d.ingestion_status, # type: ignore
            content_hash=d.content_hash,
            version=d.version,
            chunks_count=len(d.chunks),
            created_at=d.created_at
        ))
    return res

@router.post("", response_model=TrustedSourceResponse)
def register_new_source(data: TrustedSourceCreate, db: Session = Depends(get_db)):
    existing = db.query(TrustedSourceModel).filter_by(id=data.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="المصدر مسجل مسبقاً بهذا المعرّف")
    return source_registry_service.register_source(db, data)

@router.patch("/{source_id}", response_model=TrustedSourceResponse)
def update_source_details(source_id: str, data: TrustedSourceUpdate, db: Session = Depends(get_db)):
    updated = source_registry_service.update_source(db, source_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="المصدر غير موجود")
    return updated

@router.post("/{source_id}/verify", response_model=TrustedSourceResponse)
def verify_source_endorsement(
    source_id: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db)
):
    verifier_name = payload.get("verifier_name", "مراجع معتمد - بيّنة AI")
    notes = payload.get("notes")
    verified = source_registry_service.verify_source(db, source_id, verifier_name, notes)
    if not verified:
        raise HTTPException(status_code=404, detail="المصدر غير موجود")
    return verified
