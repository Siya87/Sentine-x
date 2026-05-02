@echo off
echo ========================================
echo  SentinelX AI - Backend Restart Script
echo ========================================
echo.

echo Stopping any running backend processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting backend server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --port 8000

pause

@REM Made with Bob
