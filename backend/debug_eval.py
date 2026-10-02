import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from app.services.evaluation_service import evaluation_service

async def main():
    res = await evaluation_service.run_evaluation()
    print(f"Passed: {res['passed_tests']} / {res['total_tests']} ({res['success_rate']}%)")
    for d in res['detailed_results']:
        if not d['passed']:
            print(f"- {d['id']} [{d['category']}]: Exp='{d['expected_status']}', Actual='{d['actual_status']}' | Input: {d['input_preview']}")

if __name__ == '__main__':
    asyncio.run(main())
