@echo off
title Install Ollama
echo ====================================================
echo          🦙 Installing Ollama for Windows
echo ====================================================

REM --- Check if Ollama is already installed ---
where ollama >nul 2>nul
if %errorlevel%==0 (
    echo Ollama is already installed on this system.
    pause
    exit /b
)

REM --- Download Ollama installer ---
echo Downloading Ollama installer...
powershell -Command "Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile 'OllamaSetup.exe'"

REM --- Run the installer silently ---
echo Running Ollama installer...
start /wait OllamaSetup.exe /SILENT

REM --- Clean up ---
del OllamaSetup.exe

echo.
echo ✅ Ollama installed successfully!
echo You can now run run.bat to start the dashboard.
pause
