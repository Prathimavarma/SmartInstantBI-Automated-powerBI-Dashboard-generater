@echo off
setlocal enabledelayedexpansion

REM ==============================================
REM 🚀 Portable Streamlit + Ollama Launcher
REM ==============================================
echo.
echo [🔍] Initializing environment...
echo.

REM Detect current directory (universal)
set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

REM Define requirements path
set "REQ_PATH=%APP_DIR%resources\requirements.txt"

REM Activate virtual environment
if exist "%APP_DIR%venv\Scripts\activate" (
    call "%APP_DIR%venv\Scripts\activate"
) else (
    echo [⚠️] Virtual environment not found! Please run first_time_run.bat first.
    pause
    exit /b
)

REM Start Ollama in background (non-blocking)
echo [🧠] Starting Ollama service...
start "" /min cmd /c "ollama serve >nul 2>&1"

REM Small delay to ensure Ollama is ready
timeout /t 3 >nul

REM Install missing dependencies (quiet)
if exist "%REQ_PATH%" (
    echo [📦] Checking required packages...
    pip install -r "%REQ_PATH%" --quiet
) else (
    echo [❌] requirements.txt not found in resources folder!
    pause
    exit /b
)

REM Launch Streamlit app (auto opens browser)
echo [💻] Launching Streamlit dashboard...
start "" cmd /c "streamlit run "%APP_DIR%app.py" --server.headless false --server.port 8501"

REM Open browser automatically after short wait
timeout /t 5 >nul
start http://localhost:8501

echo.
echo [✅] App launched successfully!
echo Press Ctrl + C in this window to stop the server.
echo.
pause
endlocal
