@echo off
echo Starting Delhi Civic Navigator AI Backend...
echo Backend will run on http://localhost:8000
echo.
echo DO NOT CLOSE THIS WINDOW - it keeps the server running!
echo.
cd /d "%~dp0"
.\backend\venv\Scripts\python.exe .\backend\app.py
pause
