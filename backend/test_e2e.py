import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.schemas import VerificationRequest
from app.services.verification_engine import VerificationEngine
from app.services.evidence_gate import evidence_gate

async def run_e2e_tests():
    engine = VerificationEngine()
    print("=== STARTING E2E VERIFICATION PIPELINE TESTS ===\n")
    
    # Test 1: Fake Hadith (Not in sources)
    claim_1 = "قال رسول الله صلى الله عليه وسلم: نظافة الدار تورث الغنى."
    print(f"Test 1: {claim_1}")
    req_1 = VerificationRequest(text=claim_1)
    res_1 = await engine.verify(req_1)
    print(f"Extracted Claim: {res_1.extracted_claim}")
    print(f"Status: {res_1.status_slug}")
    print(f"Evidence Count: {len(res_1.evidence)}")
    print(f"Result Reason: {res_1.reason}")
    print("-" * 40)
    
    # Test 2: EvidenceGate explicit test
    print("Test 2: EvidenceGate with unapproved injected evidence")
    fake_evidence = [{
        "source_id": "unapproved_source_123",
        "url": "https://wikipedia.org/some_islamic_page",
        "text": "This is a fact from wikipedia",
        "relevance_score": 0.99
    }]
    gate_result = evidence_gate.validate(fake_evidence, 0.95, "Test claim", "VERIFIED")
    print(f"Gate Passed: {gate_result['passed']}")
    print(f"Abstention Required: {gate_result['abstention_required']}")
    print(f"Reason: {gate_result['reason']}")
    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_e2e_tests())
