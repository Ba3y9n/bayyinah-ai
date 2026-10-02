@echo off
echo ===================================================
echo     تشغيل منصة بيّنة AI - Bayyinah AI Platform
echo           تحقّق قبل أن تنشر.
echo ===================================================

start "Bayyinah Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
start "Bayyinah Frontend (Vite/React)" cmd /k "cd frontend && npm run dev"

echo.
echo الخوادم قيد التشغيل:
echo - الواجهة الأمامية: http://localhost:3000
echo - الخادم والتوثيق: http://127.0.0.1:8000/docs
echo.
pause
