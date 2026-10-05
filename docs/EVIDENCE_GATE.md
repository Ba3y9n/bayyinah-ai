# The Evidence Gate

The **Evidence Gate** (`evidence_gate.py`) is the most critical security and reliability component of Bayyinah AI. It is an algorithmic firewall that sits between the Retrieval Engine and the Grounding LLM.

## Workflow

```text
Candidate Evidence (from Semantic Search / SerpAPI)
        ↓
Source ID validation (Does it exist?)
        ↓
Approved Allowlist Check (`official_allowlist.py`)
   ┌────┴────┐
  YES        NO
   ↓          ↓
Provenance   REJECT (Silently dropped)
   ↓
Canonical URL Check
   ↓
Evidence Accepted & Passed to Gemini
```

## Core Rules
1. **Approval Enforcement:** If a retrieved document comes from `wikipedia.org`, `islamqa.info`, or `google.com`, it is immediately rejected because its domain/ID is not in the 11-source allowlist.
2. **Snippet Rejection:** Search engine meta-descriptions (snippets) are considered volatile and prone to truncation or search engine manipulation. The Gate requires the full chunk from the actual canonical URL.
3. **Forced Abstention:** If the Evidence Gate drops all candidate evidence (resulting in 0 valid chunks), it overrides the LLM and forces the system state to `INSUFFICIENT_EVIDENCE`.
4. **No LLM Bypass:** The Grounding LLM does not have internet access. It can only read the JSON array of evidence that successfully passed the Evidence Gate.
