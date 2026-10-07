@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run Setup-Windows.cmd first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe GUI\main_without_gui.py
pause
