@echo off
REM Yandex Mentor — Server + Daemon
REM Код сервера — в пакете src/, точка входа server.py (совместимость сохранена)

set SCRIPT_DIR=%~dp0
set PYTHON=py

cd /d "%SCRIPT_DIR%"
start "Yandex Mentor" cmd /c "%PYTHON% -m uvicorn server:app --host 0.0.0.0 --port 8000 > logs\mentor.log 2>&1"

echo Yandex Mentor started.
echo Server: http://localhost:8000
echo Logs: %SCRIPT_DIR%logs\mentor.log
echo Stop: taskkill /F /IM python.exe /FI "WINDOWTITLE eq Yandex Mentor*"
