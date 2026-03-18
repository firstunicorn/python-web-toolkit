#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validates architectural boundaries using Import Linter
.DESCRIPTION
    Checks that all packages follow layered architecture rules
#>

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Python Web Toolkit - Architecture Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$workspaceRoot = Split-Path -Parent $PSScriptRoot

try {
    Push-Location $workspaceRoot
    
    Write-Host "Running Import Linter..." -ForegroundColor Yellow
    poetry run lint-imports
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ All architectural contracts passed!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Architecture violations detected!" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
