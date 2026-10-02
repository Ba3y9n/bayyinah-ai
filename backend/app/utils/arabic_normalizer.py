import re
from typing import List

# Arabic diacritics regex
TASHKEEL_REGEX = re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670\u0640]')

def remove_tashkeel(text: str) -> str:
    """Removes all Arabic diacritics, harakat, and tatweel."""
    if not text:
        return ""
    return TASHKEEL_REGEX.sub('', text)

def normalize_arabic(text: str) -> str:
    """
    Normalizes Arabic text:
    - Removes Tashkeel & Tatweel
    - Normalizes Alef forms (أ, إ, آ -> ا)
    - Normalizes Taa Marbuta (ة -> ه)
    - Normalizes Yaa (ى -> ي)
    - Replaces Quranic signs & extra spaces
    """
    if not text:
        return ""
    text = remove_tashkeel(text)
    
    # Normalize Alefs
    text = re.sub(r'[إأآٱ]', 'ا', text)
    
    # Normalize Yaa
    text = re.sub(r'[ى]', 'ي', text)
    
    # Normalize Taa Marbuta
    text = re.sub(r'[ة]', 'ه', text)
    
    # Remove special punctuation and Quranic symbols
    text = re.sub(r'[۩۝۞﴾﴿«»"\'\(\)\.,:;!؟\-\[\]]', ' ', text)
    
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_arabic(text: str) -> List[str]:
    """Tokenizes Arabic text after normalization, ignoring stop words and single characters."""
    normalized = normalize_arabic(text)
    tokens = normalized.split()
    # Simple stop words filter for search refinement
    stop_words = {
        'في', 'من', 'عن', 'على', 'إلى', 'الى', 'مع', 'هذا', 'هذه', 'ذلك', 'تلك', 
        'التي', 'الذي', 'الذين', 'هو', 'هي', 'هم', 'نحن', 'انا', 'أنا', 'ان', 'أن', 
        'انما', 'إنما', 'كان', 'يكون', 'قال', 'قالت', 'ما', 'لا', 'لم', 'لن', 'ثم', 'او', 'أو'
    }
    return [t for t in tokens if len(t) > 1 and t not in stop_words]

def compute_jaccard_similarity(text1: str, text2: str) -> float:
    """Calculates Jaccard similarity between two Arabic strings."""
    tokens1 = set(tokenize_arabic(text1))
    tokens2 = set(tokenize_arabic(text2))
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union) if union else 0.0
