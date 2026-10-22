@echo off
title Smart Job Recommendation Portal
echo =======================================================
echo    Smart Job Recommendation Portal - Development Server
echo =======================================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo Starting Django Web Server on http://127.0.0.1:8000/ ...
python manage.py runserver 127.0.0.1:8000
pause
