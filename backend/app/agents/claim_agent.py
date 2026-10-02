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
        Extracts claim, normalizes text, determines claim_type and sensitivity.
        """
        # Strip common demo or OCR wrapper prefixes if present
        prefixes = [
            "صورة بطاقة دعوية:", "صورة إنفوجرافيك:", "صورة منشور واتساب:", 
            "صورة مخطوطة مصحف:", "صورة منشور دعوي:", "صورة منشور:"
        ]
        cleaned_text = raw_text
        for p in prefixes:
            if cleaned_text.startswith(p):
                cleaned_text = cleaned_text[len(p):].strip()
                break

        normalized = normalize_arabic(cleaned_text)
        
        # Check personal fatwa / sensitivity
        personal_terms = [
            "حلفت", "زوجتي", "طلقت", "طلاق", "غضبان", "شجار", "ميراث", "ابي مات", 
            "امي ماتت", "هل يلزمني كفارة", "هل وقع", "حكم فعلي", "ذنبي", "تبت",
            "معاملة مالية", "رافعة مالية", "مقايضة", "ارباحي حلال", "أرباحي حلال", "تداول"
        ]
        is_personal = any(term in normalized for term in personal_terms) and ("؟" in raw_text or "هل" in raw_text or "ما حكم" in raw_text)
        
        sensitivity = "high" if is_personal else "low"
        requires_specialist = is_personal

        # Determine claim type
        if is_personal:
            claim_type = "PersonalCase"
        elif any(w in normalized for w in ["حكم", "واجب", "صلاه", "الفاتحه", "الجهريه", "خلف الامام", "وضوء", "صيام"]):
            claim_type = "Fiqh"
        elif any(w in normalized for w in ["قال رسول الله", "عن النبي", "سمعت رسول الله", "صلي الله عليه وسلم", "حديث", "انما الاعمال", "اطلبوا العلم", "الكلمه الطيبه", "من قال سبحان الله"]):
            claim_type = "Hadith"
        elif any(w in normalized for w in ["دعاء", "من قرا", "ليله الجمعه", "ملك يناديه", "وسع رزقه", "سبع مرات"]):
            claim_type = "Dua"
        elif any(w in normalized for w in ["قال تعالي", "قال الله", "سوره", "ايه", "فاتقوا الله", "الله لا اله الا هو"]):
            claim_type = "Quran"
        elif any(w in normalized for w in ["حكم", "واجب", "صلاه", "الفاتحه", "الجهريه", "خلف الامام", "وضوء", "صيام"]):
            claim_type = "Fiqh"
        elif any(w in normalized for w in ["هجره", "غار ثور", "ابو بكر", "غزوه", "بدر", "احد"]):
            claim_type = "Seerah"
        elif any(w in normalized for w in ["قال ابن تيميه", "قال الشافعي", "قال احمد", "قال مالك", "قال ابو حنيفه"]):
            claim_type = "ScholarQuote"
        else:
            claim_type = "GeneralReligiousClaim"

        # Extract entities and religious terms
        tokens = tokenize_arabic(raw_text)
        religious_terms = [t for t in tokens if t in [
            'صلاة', 'صيام', 'حج', 'زكاة', 'نية', 'طلاق', 'فاتحة', 'قرآن', 'حديث', 
            'نبي', 'رسول', 'صحابي', 'علم', 'صدقة', 'استطاعة', 'تقوى', 'غضب'
        ]]

        main_claim = raw_text.strip()
        if len(main_claim) > 200:
            main_claim = main_claim[:200] + "..."

        return {
            "original_text": raw_text.strip(),
            "normalized_text": normalized,
            "main_claim": main_claim,
            "claim_type": claim_type,
            "entities": tokens[:5],
            "religious_terms": religious_terms,
            "possible_references": [],
            "sensitivity": sensitivity,
            "requires_specialist": requires_specialist
        }

claim_agent = ClaimAgent()
