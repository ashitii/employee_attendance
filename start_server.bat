@echo off
cd /d "%~dp0"
set DJANGO_SETTINGS_MODULE=employee_attendance.settings
daphne employee_attendance.asgi:application
pause
