import asyncio
import json
import sys
import os

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

from app.models.schemas import VerificationRequest
from app.services.verification_engine import verification_engine

async def test_all_cases():
    print("Testing Bayyinah AI Verification Engine on all 7 cases...")
    
    with open("app/data/demo_cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    for c in cases:
        print(f"\n==========================================")
        print(f"Testing Case {c['id']}: {c['title']}")
        req = VerificationRequest(
            text=c["input_text"],
            image_base64=c.get("image_sample_url") if c.get("is_image_demo") else None
        )
        res = await verification_engine.verify(req, is_demo=True)
        print(f"-> Claim: {res.extracted_claim[:60]}")
        print(f"-> Content Type: {res.content_type_ar}")
        print(f"-> Result Status: {res.status} (Slug: {res.status_slug})")
        print(f"-> Checked Sources: {res.checked_sources_count}")
        print(f"-> Evidence Count: {len(res.evidence)}")
        print(f"-> Reason: {res.reason}")
        print(f"-> Steps Logged: {len(res.evidence_chain)}")
        
        if res.status == c["expected_status"] or res.status_slug == c["expected_slug"]:
            print(f"[OK] MATCHED EXPECTED: {c['expected_status']}")
            passed += 1
        else:
            print(f"[FAIL] Expected: {c['expected_status']}, Got: {res.status}")

    print(f"\n==========================================")
    print(f"SUMMARY: {passed}/{len(cases)} cases passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_all_cases())
