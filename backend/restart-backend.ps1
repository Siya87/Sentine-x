# SentinelX AI - Backend Restart Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SentinelX AI - Backend Restart Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Stopping any running backend processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "*uvicorn*"} | Stop-Process -Force
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

python -m uvicorn app.main:app --reload --port 8000

# Made with Bob
