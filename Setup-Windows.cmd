@echo off
setlocal
cd /d "%~dp0"
py -3.11 -c "import sys; assert sys.maxsize > 2**32" >nul 2>&1
if errorlevel 1 (
 echo Install Python 3.11 64-bit from python.org with the Python launcher enabled.
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 py -3.11 -m venv .venv
 if errorlevel 1 goto failed
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
if not exist .env copy .env.example .env >nul
.venv\Scripts\python.exe check_setup.py
if errorlevel 1 goto failed
echo Setup complete. Double-click Run-Jarvis.cmd.
pause
exit /b 0
:failed
echo Setup failed. Review the error above. You can run setup again.
pause
exit /b 1
