@echo off
echo Starting CyberDuo Full Stack...

:: Start Backend
echo Launching Backend...
cd backend
start "CyberDuo Backend" cmd /k ".\venv\Scripts\python.exe -m uvicorn app.main:app --port 5000 --reload"
cd ..

:: Start Frontend
echo Launching Frontend...
cd frontend
start "CyberDuo Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==================================================
echo System booting up. 
echo 1. Check the 'CyberDuo Backend' window for database connection.
echo 2. Check the 'CyberDuo Frontend' window for the dev server link.
echo ==================================================
pause
