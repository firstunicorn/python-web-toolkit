#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install all packages in the python-web-toolkit monorepo
.DESCRIPTION
    Iterates through all packages and runs poetry install in each one.
    This ensures all local dependencies are available for cross-referencing.
#>

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 Installing Python Web Toolkit Packages`n" -ForegroundColor Cyan

$packagesDir = Join-Path $PSScriptRoot ".." "packages"
$packages = Get-ChildItem $packagesDir -Directory

$total = $packages.Count
$current = 0

foreach ($package in $packages) {
    $current++
    $percent = [math]::Round(($current / $total) * 100)
    
    Write-Host "[$current/$total] Installing $($package.Name)..." -ForegroundColor Yellow
    
    Push-Location $package.FullName
    
    try {
        poetry install --quiet 2>&1 | Out-Null
        Write-Host "  ✅ $($package.Name) installed" -ForegroundColor Green
    }
    catch {
        Write-Host "  ❌ Failed to install $($package.Name): $_" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

Write-Host "`n✨ Installation complete!`n" -ForegroundColor Cyan
Write-Host "Run " -NoNewline
Write-Host ".\scripts\test-all.ps1" -ForegroundColor Yellow -NoNewline
Write-Host " to test all packages"
