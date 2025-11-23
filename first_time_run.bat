@echo off
setlocal enabledelayedexpansion

REM ==============================================
REM ⚙️ First Time Setup Script (Portable Installer)
REM ==============================================
echo.
echo [🚀] Setting up your environment for Data Bot...
echo.

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"
set "REQ_PATH=%APP_DIR%resources\requirements.txt"

REM Step 1: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [❌] Python not found! Please install Python 3.9+ and rerun this script.
    pause
    exit /b
)

REM Step 2: Create virtual environment if missing
if not exist "%APP_DIR%venv\" (
    echo [🔧] Creating virtual environment...
    python -m venv "%APP_DIR%venv"
)

REM Step 3: Activate environment
call "%APP_DIR%venv\Scripts\activate"

REM Step 4: Install dependencies
if exist "%REQ_PATH%" (
    echo [📦] Installing Python dependencies...
    pip install --upgrade pip
    pip install -r "%REQ_PATH%"
) else (
    echo [❌] requirements.txt not found in resources folder!
    pause
    exit /b
)

REM Step 5: Install Ollama if missing
where ollama >nul 2>&1
if errorlevel 1 (
    echo [🧠] Installing Ollama...
    powershell -Command "Invoke-WebRequest https://ollama.com/download/OllamaSetup.exe -OutFile ollama_setup.exe"
    start /wait ollama_setup.exe
    del ollama_setup.exe
)

REM Step 6: Pull model (small one if on low-end system)
echo [🤖] Checking for Gemma model...
ollama list | findstr /i "gemma3:1b" >nul
if errorlevel 1 (
    echo [⬇️] Downloading Gemma3:1b model...
    ollama pull gemma3:1b
) else (
    echo [✅] Gemma3:1b model already available!
)

echo.
echo [✅] Setup completed successfully!
echo You can now run the app using run.bat
echo.
pause
endlocal
