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

Write-Host "[private-ai-companion] Running release validation..."

Invoke-Checked "ruff format" { uv run --locked ruff format --check }
Invoke-Checked "ruff check" { uv run --locked ruff check }
Invoke-Checked "pytest" { uv run --locked pytest }
Invoke-Checked "pyright" { uv run --locked pyright }
Invoke-Checked "uv build" { uv build --sdist --wheel }

Write-Host "[private-ai-companion] Validating Windows launcher diagnostics path..."
Invoke-Checked "Start.bat diagnostics" { cmd /c Start.bat --diagnostics }

Write-Host "[private-ai-companion] Release validation completed."
