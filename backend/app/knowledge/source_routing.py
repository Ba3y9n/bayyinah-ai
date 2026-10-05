from typing import List, Dict, Any, Optional

class SourceRoutingService:
    """
    Intelligent Domain-to-Source Router.
    Ensures targeted evidence retrieval based on scientific domain:
    - QURAN -> King Fahd Complex, Quranpedia
    - HADITH -> Sahih Bukhari, Sahih Muslim, Dorar Net
    - TAFSEER -> Tafsir Ibn Kathir, Dorar Net
    - AQEEDAH -> Dorar Net, General Scholars
    - FIQH -> Dorar Net, Majmoo al-Fatawa, IslamQA, Islamweb
    - SEERAH_HISTORY -> Shamela, Ar-Raheeq Al-Makhtum, Dorar Net
    - QUESTIONS_DOUBTS -> Dawa Center (file/7937)
    - DICTIONARY_TRANSLATION -> Islamic Content / Al-Jumhrah Dictionary
    - DAWA -> Dawa Center, Islamic Content
    """

    DOMAIN_TO_SOURCE_IDS = {
        "QURAN": ["src-quran-complex", "src-quranpedia"],
        "HADITH": ["src-bukhari", "src-muslim", "src-dorar-hadith", "src-dorar-net"],
        "TAFSEER": ["src-tafsir-ibn-kathir", "src-dorar-net"],
        "AQEEDAH": ["src-dorar-net", "src-general-scholars"],
        "FIQH": ["src-majmoo-fatawa", "src-dorar-net", "src-general-scholars", "src-islamqa", "src-islamweb"],
        "SEERAH_HISTORY": ["src-seerah-rahik", "src-shamela-ws", "src-dorar-net"],
        "QUESTIONS_DOUBTS": ["src-dawa-center-7937", "src-dawa-center"],
        "DICTIONARY_TRANSLATION": ["src-islamic-content-dict", "src-islamic-content"],
        "DAWA": ["src-dawa-center", "src-islamic-content"]
    }

    CLAIM_TYPE_TO_DOMAIN = {
        "QURAN_VERSE": "QURAN",
        "HADITH": "HADITH",
        "HADITH_ATTRIBUTION": "HADITH",
        "HADITH_CLAIM": "HADITH",
        "TAFSEER": "TAFSEER",
        "AQEEDAH": "AQEEDAH",
        "AQEEDAH_CLAIM": "AQEEDAH",
        "FIQH": "FIQH",
        "FIQH_CLAIM": "FIQH",
        "SEERAH": "SEERAH_HISTORY",
        "HISTORY": "SEERAH_HISTORY",
        "HISTORICAL_CLAIM": "SEERAH_HISTORY",
        "SEERAH_HISTORY": "SEERAH_HISTORY",
        "QUESTIONS_DOUBTS": "QUESTIONS_DOUBTS",
        "DOUBT": "QUESTIONS_DOUBTS",
        "QUESTION": "QUESTIONS_DOUBTS",
        "DAWAH": "DAWA",
        "DAWA": "DAWA",
        "DAWA_CONTENT": "DAWA",
        "TRANSLATION": "DICTIONARY_TRANSLATION",
        "TERM": "DICTIONARY_TRANSLATION",
        "DEFINITION": "DICTIONARY_TRANSLATION",
        "DICTIONARY_TRANSLATION": "DICTIONARY_TRANSLATION",
        "PERSONAL_CASE": "FIQH",
        "PERSONAL_FATWA": "FIQH"
    }

    def route_query(self, category: Optional[str] = None, claim_type: Optional[str] = None) -> List[str]:
        """
        Returns the prioritized list of trusted source IDs suitable for this inquiry.
        """
        cat_upper = (category or "").upper()
        type_upper = (claim_type or "").upper()

        target_domain = None
        if cat_upper in self.DOMAIN_TO_SOURCE_IDS:
            target_domain = cat_upper
        elif type_upper in self.CLAIM_TYPE_TO_DOMAIN:
            target_domain = self.CLAIM_TYPE_TO_DOMAIN[type_upper]

        if target_domain and target_domain in self.DOMAIN_TO_SOURCE_IDS:
            return self.DOMAIN_TO_SOURCE_IDS[target_domain]

        # Default fallback to all primary sources
        return []

source_routing_service = SourceRoutingService()
