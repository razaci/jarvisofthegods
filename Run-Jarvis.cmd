@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run Setup-Windows.cmd first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe GUI\main.py
if errorlevel 1 (
 echo Jarvis stopped with an error. Review the details above.
 pause
 exit /b 1
)
