# Evaluation Guide for Judges

This document explicitly maps the features of **Bayyinah AI** to standard technical and competition evaluation criteria.

### 1. Technical & AI Architecture
* **Gemini Native Integration:** We utilize Gemini 2.5 Flash / 3.8 Flash for advanced multimodal understanding, leveraging the Gemini Files API for long-form video transcripts and Gemini Vision for OCR.
* **Strict RAG (Retrieval-Augmented Generation):** The system uses a pure RAG approach where the LLM is forcibly decoupled from its internal weights when providing answers. 
* **Hybrid Search:** Combines semantic vector search (`pgvector` via `text-embedding-004`) with exact keyword matching to ensure maximum recall from classical Arabic texts.
* **Evidence Gate:** A hard-coded algorithmic layer that physically drops any context chunks that do not possess a trusted `source_id`.

### 2. Operational Realism
* **Production-Grade Database:** Uses Supabase PostgreSQL. There are no silent fallbacks to SQLite in production.
* **Stateless API:** FastAPI backend built for serverless deployment on Vercel or AWS Lambda.
* **API Constraints & Backoff:** Implements robust error handling for `429 RESOURCE_EXHAUSTED` quotas without crashing the application.

### 3. Reliability & Trust
* **Zero-Hallucination Grounding:** If the 11 approved sources do not contain the answer, the system defaults to `INSUFFICIENT_EVIDENCE`. It will never say "False" just because it couldn't find it, and it will never invent a citation.
* **Provenance Verification:** Every single piece of evidence returned to the user contains a `source_name`, `canonical_url`, and the exact `excerpt` matched. 
* **Conflict Detection:** The system detects when two approved sources have differing scholarly opinions (e.g., Fiqh vs. contemporary Fatwa) and flags the result as `CONFLICT` rather than forcing a middle ground.

### 4. Innovation
* **Evidence-First Multimodal Verification:** Unlike typical text-based fact-checkers, Bayyinah AI allows users to upload a TikTok video or an Instagram image, extracts the Islamic claims from the visual/audio content, and verifies them seamlessly.
* **Honest Capability Resolution:** If a social media URL (X / TikTok) blocks the scraper or API, the system does not hallucinate from the URL slug. It throws an `ACCESS_LIMITED` flag and prompts the user to upload the video directly.

### 5. Presentation & UX
* **Evidence-Bound UI:** The frontend presents the user with the Claim, the Verdict, and the exact Evidence cards. 
* **Arabic-First Design:** Polished RTL interface optimized for readability of Arabic scholarly texts (using modern typefaces and appropriate cultural UI motifs like Saudi Green and Gold).
