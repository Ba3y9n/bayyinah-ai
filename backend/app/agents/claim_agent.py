from typing import Dict, Any, List
from ..utils.arabic_normalizer import normalize_arabic, tokenize_arabic
from ..config import settings

class ClaimAgent:
    """
    AI JOB 1 & 2: Multimodal Content Understanding & Claim Extraction Agent
    Converts user input text or multimodal OCR result into a structured, searchable claim.
    """
    SYSTEM_INSTRUCTION = (
        "أنت وكيل استخراج الادعاءات في منصة بيّنة AI. مهمتك فهم المحتوى الإسلامي المدخل، "
        "وتجريده من الصياغات التعبيرية غير المؤثرة، واستخراج الادعاء الأساسي المطلوب إثباته أو نفيه، "
        "وتصنيف نوع المحتوى، وتحديد حساسية النص إن كان يتطلب استفساراً شخصياً أو إحالة لمختص."
    )

    def __init__(self):
        pass

    def process(self, raw_text: str, is_image: bool = False) -> Dict[str, Any]:
        """
        Extracts claim using Gemini 3.8 Flash (structured Pydantic ClaimExtraction)
        with deterministic normalization fallback.
        """
        from ..services.gemini_service import gemini_service
        
        # Strip common visual/demo label prefixes if present
        prefixes = [
            "صورة بطاقة دعوية:", "صورة إنفوجرافيك:", "صورة منشور واتساب:", 
            "صورة مخطوطة مصحف:", "صورة منشور دعوي:", "صورة منشور:"
        ]
        cleaned_text = raw_text
        for p in prefixes:
            if cleaned_text.startswith(p):
                cleaned_text = cleaned_text[len(p):].strip()
                break

        # Call Gemini 3.8 Flash structured claim extraction
        claim_obj = gemini_service.extract_claim_structured(cleaned_text)
        return claim_obj.model_dump()

    def extract_multi_claims(self, raw_text: str) -> List[Any]:
        """
        Detects multiple distinct claims in a single user input or transcript.
        Returns a list of MultiClaimItem instances.
        """
        import re
        from ..models.schemas import MultiClaimItem

        cleaned = raw_text.strip()
        lines = [l.strip() for l in cleaned.splitlines() if l.strip()]
        detected_claims: List[str] = []

        numbered_pattern = re.compile(r'^(?:[0-9]+[\.\-\)]|[•\-\*]|أولاً[:\s]|ثانياً[:\s]|ثالثاً[:\s]|رابعاً[:\s])\s*(.+)$')
        for line in lines:
            match = numbered_pattern.match(line)
            if match:
                c = match.group(1).strip()
                if len(c) > 10:
                    detected_claims.append(c)
            elif len(lines) > 1 and len(line) > 20 and any(w in line for w in ["حديث", "قال", "سورة", "آية", "حكم"]):
                detected_claims.append(line)

        if len(detected_claims) <= 1:
            return [
                MultiClaimItem(
                    claim_index=1,
                    claim_text=cleaned[:250],
                    content_type="GeneralClaim",
                    is_visual=False
                )
            ]

        items = []
        for idx, c_text in enumerate(detected_claims, start=1):
            items.append(
                MultiClaimItem(
                    claim_index=idx,
                    claim_text=c_text,
                    content_type="Hadith" if any(w in c_text for w in ["حديث", "قال رسول الله", "صلى الله عليه وسلم"]) else "GeneralClaim",
                    is_visual=False
                )
            )
        return items

    def extract_claims_from_pdf_pages(self, pages_data: List[Dict[str, Any]], filename: str = "document.pdf") -> List[Any]:
        """
        Extracts claims from PDF page structure with provenance tracking:
        - file_name
        - page_number
        - extracted_excerpt
        - claim_text
        """
        from ..models.schemas import MultiClaimItem
        import re

        items: List[MultiClaimItem] = []
        global_index = 1

        for page in pages_data:
            p_num = page.get("page_number", 1)
            p_text = (page.get("text") or "").strip()
            if not p_text or len(p_text) < 10:
                continue

            lines = [l.strip() for l in p_text.splitlines() if l.strip()]
            page_claims: List[str] = []

            numbered_pattern = re.compile(r'^(?:[0-9]+[\.\-\)]|[•\-\*]|أولاً[:\s]|ثانياً[:\s]|ثالثاً[:\s]|رابعاً[:\s])\s*(.+)$')
            for line in lines:
                match = numbered_pattern.match(line)
                if match:
                    c = match.group(1).strip()
                    if len(c) > 10:
                        page_claims.append(c)
                elif len(line) > 20 and any(w in line for w in ["حديث", "قال رسول الله", "صلى الله عليه وسلم", "سورة", "آية", "حكم", "فتوى", "مذهب"]):
                    page_claims.append(line)

            if not page_claims:
                page_claims = [p_text[:250]]

            for c_text in page_claims:
                ctype = "Hadith" if any(w in c_text for w in ["حديث", "قال رسول الله", "صلى الله عليه وسلم"]) else (
                    "Quran" if any(w in c_text for w in ["سورة", "آية", "القرآن"]) else "GeneralClaim"
                )
                items.append(
                    MultiClaimItem(
                        claim_index=global_index,
                        claim_text=c_text,
                        content_type=ctype,
                        file_name=filename,
                        page_number=p_num,
                        page_start=p_num,
                        page_end=p_num,
                        extracted_excerpt=p_text[:400],
                        is_visual=False
                    )
                )
                global_index += 1

        if not items and pages_data:
            p1_text = pages_data[0].get("text", "") or "وثيقة مرفوعة"
            items.append(
                MultiClaimItem(
                    claim_index=1,
                    claim_text=p1_text[:250],
                    content_type="GeneralClaim",
                    file_name=filename,
                    page_number=1,
                    page_start=1,
                    page_end=1,
                    extracted_excerpt=p1_text[:400],
                    is_visual=False
                )
            )

        return items

claim_agent = ClaimAgent()
