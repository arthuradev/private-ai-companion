@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "LAUNCHER_LOG_DIR=logs"
set "LAUNCHER_LOG=%LAUNCHER_LOG_DIR%\startup.log"

if not exist "%LAUNCHER_LOG_DIR%" (
    mkdir "%LAUNCHER_LOG_DIR%" >nul 2>nul
    if errorlevel 1 (
        echo [private-ai-companion] Could not create logs directory.
        echo [private-ai-companion] Check permissions and run Start.bat again.
        exit /b 1
    )
)

call :log ""
call :log "[private-ai-companion] Starting..."
call :log "[private-ai-companion] Checking launcher requirements..."

where uv >nul 2>nul
if errorlevel 1 (
    call :log ""
    call :log "[private-ai-companion] uv was not found."
    call :log "[private-ai-companion] Install uv from https://docs.astral.sh/uv/ and run Start.bat again."
    call :log ""
    exit /b 1
)

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>nul
if errorlevel 1 (
    call :log ""
    call :log "[private-ai-companion] Python 3.12 or newer was not found by the Windows py launcher."
    call :log "[private-ai-companion] Install Python 3.12+ and run Start.bat again."
    call :log ""
    exit /b 1
)

if exist ".env" (
    call :log "[private-ai-companion] Found .env file. Secrets stay local and are not logged."
) else (
    call :log "[private-ai-companion] No .env file found. Continuing with safe local defaults."
    call :log "[private-ai-companion] Copy .env.example to .env only when external providers are needed."
)

call :log "[private-ai-companion] Optional providers are disabled unless configured."
call :log "[private-ai-companion] uv will sync locked dependencies if needed."
call :log "[private-ai-companion] Launching official Python entrypoint..."
call :log ""

uv run --locked private-ai-companion %*
set "APP_EXIT_CODE=%ERRORLEVEL%"

if not "%APP_EXIT_CODE%"=="0" (
    call :log ""
    call :log "[private-ai-companion] Startup failed with exit code %APP_EXIT_CODE%."
    call :log "[private-ai-companion] Check the console output and %LAUNCHER_LOG% for startup details."
) else (
    call :log ""
    call :log "[private-ai-companion] Application exited successfully."
)

exit /b %APP_EXIT_CODE%

:log
if "%~1"=="" (
    echo.
    >>"%LAUNCHER_LOG%" echo.
) else (
    echo %~1
    >>"%LAUNCHER_LOG%" echo [%DATE% %TIME%] %~1
)
exit /b 0
