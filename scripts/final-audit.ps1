$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Label,
        [Parameter(Mandatory = $true)]
        [scriptblock] $Command
    )

    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE."
    }
}

Write-Host "[private-ai-companion] Running final hardening audit..."

Invoke-Checked "release-check" {
    powershell -ExecutionPolicy Bypass -File scripts\release-check.ps1
}
Invoke-Checked "git diff check" { git diff --check }

Invoke-Checked "git ls-files" { $script:trackedFiles = git ls-files }
$forbiddenTracked = $trackedFiles | Where-Object {
    $_ -eq "PROMPT-CODEX.md" -or
    $_ -match "^(data|logs|dist|build|\.venv|\.pytest_cache|\.ruff_cache|\.pyright)/" -or
    $_ -match "(^|/)\.env$" -or
    $_ -match "\.(pem|key|p12|pfx|sqlite|sqlite3|db)$"
}

if ($forbiddenTracked) {
    Write-Host "[private-ai-companion] Forbidden tracked files detected:"
    $forbiddenTracked | ForEach-Object { Write-Host " - $_" }
    throw "Final audit failed because private/runtime artifacts are tracked."
}

$launcherText = Get-Content -Raw Start.bat
if ($launcherText -match "call :log %\*" -or $launcherText -match "echo %\*") {
    throw "Final audit failed because Start.bat would log raw CLI arguments."
}

Write-Host "[private-ai-companion] Final hardening audit completed."
