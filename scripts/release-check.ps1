$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "[private-ai-companion] Running release validation..."

uv run --locked ruff format --check
uv run --locked ruff check
uv run --locked pytest
uv run --locked pyright
uv build --sdist --wheel

Write-Host "[private-ai-companion] Validating Windows launcher diagnostics path..."
cmd /c Start.bat --diagnostics

Write-Host "[private-ai-companion] Release validation completed."
