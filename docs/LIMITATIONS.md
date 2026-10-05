# Known Limitations & Transparency

At Bayyinah AI, transparency is a feature. We do not hide edge cases or system boundaries.

### 1. Social Media Scrape Limits (TikTok & X)
If our API tokens (Bearer Tokens or OAuth) do not have sufficient privileges, or if a user's account is private, Bayyinah AI cannot read the content. 
* **Action:** The system will honestly return an `ACCESS_LIMITED` status and politely ask the user to manually upload a screenshot or screen recording. We **never** hallucinate verification based merely on the video's URL slug or metadata title.

### 2. Gemini API Quotas
We utilize Google Gemini APIs. The free tier has strict limits (e.g., `429 RESOURCE_EXHAUSTED` at 20 requests/day/model). 
* **Action:** If the quota is exhausted, the Live AI Verification will gracefully fail. The system handles this error and communicates it clearly rather than crashing.

### 3. Personal Fatwas
Bayyinah AI is a verification engine for general claims. It is not designed to issue personal Fatwas.
* **Action:** Queries involving personal divorce cases, medical issues tied to Islamic rulings, inheritance calculations, or individual disputes are flagged. The system provides available scholarly texts but mandates a `SPECIALIST_REVIEW` warning.

### 4. Insufficient Evidence
If the 11 approved sources do not contain the specific phrase or concept, the system returns `INSUFFICIENT_EVIDENCE`.
* **Action:** It does not mean the claim is inherently false (`FABRICATED`). It simply means: *"لم نجد في المصادر المعتمدة التي تم فحصها ما يثبت هذا النص"*. We prioritize scholarly integrity over pretending to know everything.
