import json
import os
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any

from .config import settings
from .models.schemas import (
    VerificationRequest, 
    VerificationResponse, 
    AssistantQuestionRequest, 
    AssistantQuestionResponse,
    SourceRegistryItem,
    DemoCase
)
from .services.verification_engine import verification_engine
from .services.registry_service import registry_service
from .services.assistant_service import assistant_service
from .services.search_service import search_service
from .services.evaluation_service import evaluation_service
from .agents.claim_agent import claim_agent
from .agents.evidence_agent import evidence_agent
from .agents.retrieval_agent import retrieval_agent
from .agents.assistant_agent import assistant_agent

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="منصة بيّنة AI للتحقق من المحتوى الإسلامي الرقمي - المسار الرابع: أدوات المعرفة والتحقق لتمكين المعرفين بالإسلام.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
verification_store: Dict[str, VerificationResponse] = {}

# 1. Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "slogan": settings.PROJECT_SLOGAN,
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "sources_count": len(registry_service.get_all_sources()),
        "documents_count": len(search_service.documents)
    }

# 2. POST /api/verify
@app.post("/api/verify", response_model=VerificationResponse)
async def verify_content(req: VerificationRequest):
    if not req.text and not req.image_base64:
        raise HTTPException(status_code=400, detail="يرجى إدخال نص أو رفع صورة للتحقق منها.")
    try:
        result = await verification_engine.verify(req, is_demo=False)
        verification_store[result.claim_id] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء فحص المحتوى: {str(e)}")

# 3. POST /api/verify/image
@app.post("/api/verify/image", response_model=VerificationResponse)
async def verify_image_content(req: VerificationRequest):
    if not req.image_base64:
        raise HTTPException(status_code=400, detail="يرجى إرفاق صورة صالحة للتحقق.")
    try:
        result = await verification_engine.verify(req, is_demo=False)
        verification_store[result.claim_id] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل التحقق البصري: {str(e)}")

# 4. POST /api/claims/extract
@app.post("/api/claims/extract")
async def extract_claim_endpoint(payload: Dict[str, Any] = Body(...)):
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="النص مطلوب لاستخراج الادعاء.")
    return claim_agent.process(text)

# 5. POST /api/search
@app.post("/api/search")
async def search_endpoint(payload: Dict[str, Any] = Body(...)):
    query = payload.get("query", "")
    category = payload.get("category", "all")
    if not query:
        raise HTTPException(status_code=400, detail="استعلام البحث مطلوب.")
    return retrieval_agent.search_keyword(query, category)

# 6. POST /api/search/hybrid
@app.post("/api/search/hybrid")
async def hybrid_search_endpoint(payload: Dict[str, Any] = Body(...)):
    queries = payload.get("queries", [])
    if isinstance(queries, str):
        queries = [queries]
    if not queries:
        raise HTTPException(status_code=400, detail="قائمة الاستعلامات مطلوبة.")
    return retrieval_agent.orchestrate_hybrid_retrieval(queries)

# 7. POST /api/evidence/validate
@app.post("/api/evidence/validate")
async def validate_evidence_endpoint(payload: Dict[str, Any] = Body(...)):
    claim = payload.get("claim", "")
    evidence_list = payload.get("evidence", [])
    return evidence_agent.validate(claim, evidence_list)

# 8. GET /api/sources
@app.get("/api/sources", response_model=List[SourceRegistryItem])
async def get_sources(category: Optional[str] = Query("all")):
    return registry_service.get_sources_by_category(category)

# 9. GET /api/sources/{id}
@app.get("/api/sources/{source_id}", response_model=SourceRegistryItem)
async def get_source_by_id(source_id: str):
    src = registry_service.get_source_by_id(source_id)
    if not src:
        raise HTTPException(status_code=404, detail="المصدر غير موجود في السجل.")
    return src

# 10. POST /api/assistant
@app.post("/api/assistant", response_model=AssistantQuestionResponse)
async def ask_assistant_endpoint(req: AssistantQuestionRequest):
    try:
        return await assistant_agent.answer(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء إجابة المساعد: {str(e)}")

# Alias for compatibility with previous client
@app.post("/api/assistant/ask", response_model=AssistantQuestionResponse)
async def ask_assistant_alias(req: AssistantQuestionRequest):
    return await assistant_agent.answer(req)

# 11. GET /api/verification/{id}
@app.get("/api/verification/{verification_id}", response_model=VerificationResponse)
async def get_verification_by_id(verification_id: str):
    if verification_id in verification_store:
        return verification_store[verification_id]
    raise HTTPException(status_code=404, detail="سجل التحقق غير موجود.")

# 12. Evaluation Endpoints (Section 44)
@app.get("/api/evaluation")
async def get_evaluation_metrics():
    """Returns cached/latest calculated evaluation metrics over the 30 test cases."""
    return await evaluation_service.run_evaluation()

@app.post("/api/evaluation/run")
async def run_evaluation_suite():
    """Executes live testing suite across the 30 evaluation cases."""
    return await evaluation_service.run_evaluation()

@app.get("/api/evaluation/dataset")
async def get_evaluation_dataset():
    """Returns the 30 test cases dataset."""
    return evaluation_service.load_dataset()

# 13. Demo Cases Endpoint
@app.get("/api/demo-cases", response_model=List[DemoCase])
async def get_demo_cases():
    demo_path = os.path.join(DATA_DIR, "demo_cases.json")
    if os.path.exists(demo_path):
        with open(demo_path, "r", encoding="utf-8") as f:
            cases = json.load(f)
            return [DemoCase(**c) for c in cases]
    return []

@app.post("/api/verify/demo/{case_id}", response_model=VerificationResponse)
async def verify_demo_case(case_id: str):
    demo_path = os.path.join(DATA_DIR, "demo_cases.json")
    if not os.path.exists(demo_path):
        raise HTTPException(status_code=404, detail="حالات الاختبار التجريبية غير متوفرة.")
    with open(demo_path, "r", encoding="utf-8") as f:
        cases = json.load(f)
        matched = next((c for c in cases if c["id"] == case_id), None)
        if not matched:
            raise HTTPException(status_code=404, detail="حالة الاختبار غير موجودة.")
        req = VerificationRequest(
            text=matched["input_text"],
            image_base64=matched.get("image_sample_url") if matched.get("is_image_demo") else None
        )
        res = await verification_engine.verify(req, is_demo=True)
        verification_store[res.claim_id] = res
        return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
