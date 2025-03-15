@echo off
cd /d "%~dp0"
set FLASK_ENV=production
set PYTHONPATH=%~dp0
python app.py
pause 