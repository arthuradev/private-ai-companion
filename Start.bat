@echo off
setlocal

cd /d "%~dp0"

echo.
echo [private-ai-companion] Starting...
echo [private-ai-companion] Checking launcher requirements...

where uv >nul 2>nul
if errorlevel 1 (
    echo.
    echo [private-ai-companion] uv was not found.
    echo Install uv from https://docs.astral.sh/uv/ and run Start.bat again.
    echo.
    exit /b 1
)

py -3.12 --version >nul 2>nul
if errorlevel 1 (
    echo.
    echo [private-ai-companion] Python 3.12 was not found by the Windows py launcher.
    echo Install Python 3.12 or newer, then run Start.bat again.
    echo.
    exit /b 1
)

echo [private-ai-companion] Environment looks ready.
echo [private-ai-companion] Launching official Python entrypoint...
echo.

uv run private-ai-companion %*
set "APP_EXIT_CODE=%ERRORLEVEL%"

if not "%APP_EXIT_CODE%"=="0" (
    echo.
    echo [private-ai-companion] Startup failed with exit code %APP_EXIT_CODE%.
    echo Check the messages above for details.
)

exit /b %APP_EXIT_CODE%
