import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.knowledge_models import TrustedSourceModel, DocumentModel, DocumentChunkModel
from ..models.knowledge_schemas import KnowledgeSearchRequest
from .retrieval_service import knowledge_retrieval_service
from .source_registry import source_registry_service
from .evidence_service import evidence_validation_service
from .specialized_handlers import quran_special_handler, terminology_special_handler

def get_knowledge_tools_definitions() -> List[Dict[str, Any]]:
    """
    Returns declarations for the 9 Knowledge Base tools for Gemini 3.8 Flash.
    """
    return [
        {
            "name": "search_knowledge_base",
            "description": "Searches the official Bayyinah AI Trusted Knowledge Base using Hybrid Search (Exact + Keyword + Semantic).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query or phrase to look up in the trusted index"},
                    "category": {"type": "string", "description": "Optional category filter: QURAN, HADITH, FIQH, DAWA, AQEEDAH, DICTIONARY_TRANSLATION, or all"},
                    "top_k": {"type": "integer", "description": "Number of top results to retrieve (default 5)"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_source_metadata",
            "description": "Retrieves comprehensive metadata, governance status, and licensing of a registered trusted source.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_id": {"type": "string", "description": "Unique identifier of the source (e.g. src-dorar-net, src-bukhari)"}
                },
                "required": ["source_id"]
            }
        },
        {
            "name": "get_document_metadata",
            "description": "Retrieves document information, canonical publisher, and content hash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "Unique identifier of the document"}
                },
                "required": ["document_id"]
            }
        },
        {
            "name": "retrieve_evidence",
            "description": "Retrieves candidate evidence chunks enriched with exact provenance and locator details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_text": {"type": "string", "description": "The normalized claim text to retrieve evidence for"},
                    "category": {"type": "string", "description": "Category: QURAN, HADITH, FIQH, DAWA, etc."}
                },
                "required": ["claim_text"]
            }
        },
        {
            "name": "verify_claim_against_evidence",
            "description": "Applies verification governance rules against retrieved evidence, returning status, level, and abstention note if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_text": {"type": "string", "description": "Extracted claim text"},
                    "claim_type": {"type": "string", "description": "Claim type: QURAN_VERSE, HADITH_CLAIM, PERSONAL_FATWA, etc."},
                    "category": {"type": "string", "description": "Category domain"}
                },
                "required": ["claim_text", "claim_type", "category"]
            }
        },
        {
            "name": "detect_conflicting_evidence",
            "description": "Checks if the retrieved evidence contains multiple scholarly viewpoints or legitimate disagreements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic or legal issue to check for differences"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_term_definition",
            "description": "Retrieves the standardized definition and approved multi-lingual translations of an Islamic term from Al-Jumhrah / Islamic Content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {"type": "string", "description": "Arabic term (e.g. التوحيد, الشرك, البدعة, الجهاد)"}
                },
                "required": ["term"]
            }
        },
        {
            "name": "get_quran_reference",
            "description": "Performs exact verse inspection against the King Fahd Quran Complex scripture database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Quranic verse or fragment"}
                },
                "required": ["text"]
            }
        },
        {
            "name": "get_hadith_reference",
            "description": "Retrieves authenticated Hadith by matn with Sahih Bukhari, Sahih Muslim, and Dorar Net takhrij.",
            "parameters": {
                "type": "object",
                "properties": {
                    "matn": {"type": "string", "description": "Prophetic tradition matn or keywords"}
                },
                "required": ["matn"]
            }
        }
    ]


class KnowledgeToolsDispatcher:
    """
    Executes real database queries for Gemini Function Calls with zero mock responses.
    """

    def dispatch(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        db: Session = SessionLocal()
        try:
            if tool_name == "search_knowledge_base":
                req = KnowledgeSearchRequest(
                    query=args.get("query", ""),
                    category=args.get("category", "all"),
                    top_k=args.get("top_k", 5)
                )
                res = knowledge_retrieval_service.search(db, req)
                return res.model_dump()

            elif tool_name == "get_source_metadata":
                src = source_registry_service.get_source_by_id(db, args.get("source_id", ""))
                return src.model_dump() if src else {"error": "Source not found in registry"}

            elif tool_name == "get_document_metadata":
                doc = db.query(DocumentModel).filter_by(id=args.get("document_id", "")).first()
                if doc:
                    return {
                        "id": doc.id,
                        "title_ar": doc.title_ar,
                        "source_id": doc.source_id,
                        "category": doc.category,
                        "official_url": doc.official_url,
                        "content_hash": doc.content_hash,
                        "version": doc.version
                    }
                return {"error": "Document not found"}

            elif tool_name == "retrieve_evidence":
                req = KnowledgeSearchRequest(
                    query=args.get("claim_text", ""),
                    category=args.get("category", "all"),
                    top_k=5
                )
                res = knowledge_retrieval_service.search(db, req)
                return {"evidence_candidates": [r.model_dump() for r in res.results]}

            elif tool_name == "verify_claim_against_evidence":
                claim = args.get("claim_text", "")
                cat = args.get("category", "all")
                ctype = args.get("claim_type", "OTHER")
                req = KnowledgeSearchRequest(query=claim, category=cat, top_k=5)
                search_res = knowledge_retrieval_service.search(db, req)
                val_res = evidence_validation_service.validate(db, claim, ctype, cat, search_res.results)
                # Ensure JSON serializable
                if "primary_evidence" in val_res and hasattr(val_res["primary_evidence"], "model_dump"):
                    val_res["primary_evidence"] = val_res["primary_evidence"].model_dump()
                return val_res

            elif tool_name == "detect_conflicting_evidence":
                req = KnowledgeSearchRequest(query=args.get("query", ""), category="FIQH", top_k=5)
                search_res = knowledge_retrieval_service.search(db, req)
                has_conflict = any("خلاف" in r.chunk.get("content", "") for r in search_res.results)
                return {
                    "topic": args.get("query"),
                    "has_conflict": has_conflict,
                    "excerpts": [r.chunk.get("content") for r in search_res.results if "خلاف" in r.chunk.get("content", "")]
                }

            elif tool_name == "get_term_definition":
                term_info = terminology_special_handler.lookup_term(db, args.get("term", ""))
                return term_info or {"error": "Term not registered in standard terminology index"}

            elif tool_name == "get_quran_reference":
                q_res = quran_special_handler.inspect_verse(db, args.get("text", ""))
                return q_res or {"error": "Verse not matched in primary Quran corpus"}

            elif tool_name == "get_hadith_reference":
                req = KnowledgeSearchRequest(query=args.get("matn", ""), category="HADITH", top_k=3)
                search_res = knowledge_retrieval_service.search(db, req)
                return {"matches": [r.model_dump() for r in search_res.results]}

            else:
                return {"error": f"Unknown tool name: {tool_name}"}

        finally:
            db.close()

knowledge_tools_dispatcher = KnowledgeToolsDispatcher()
