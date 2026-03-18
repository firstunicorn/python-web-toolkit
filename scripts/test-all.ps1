#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run tests for all packages in the python-web-toolkit monorepo
.DESCRIPTION
    Iterates through all packages and runs pytest in each one.
    Displays a summary at the end.
#>

$ErrorActionPreference = "Stop"

Write-Host "`n🧪 Testing Python Web Toolkit Packages`n" -ForegroundColor Cyan

$packagesDir = Join-Path $PSScriptRoot ".." "packages"
$packages = Get-ChildItem $packagesDir -Directory

$results = @()
$total = $packages.Count
$current = 0

foreach ($package in $packages) {
    $current++
    
    Write-Host "`n=== [$current/$total] Testing $($package.Name) ===" -ForegroundColor Cyan
    
    Push-Location $package.FullName
    
    try {
        $output = poetry run pytest -v --tb=line -q 2>&1 | Out-String
        
        # Extract pass/fail counts
        if ($output -match "(\d+) passed") {
            $passed = $Matches[1]
            $results += [PSCustomObject]@{
                Package = $package.Name
                Status = "✅ PASS"
                Tests = "$passed passed"
                Color = "Green"
            }
            Write-Host "  ✅ $passed tests passed" -ForegroundColor Green
        }
        elseif ($output -match "(\d+) failed") {
            $failed = $Matches[1]
            $results += [PSCustomObject]@{
                Package = $package.Name
                Status = "❌ FAIL"
                Tests = "$failed failed"
                Color = "Red"
            }
            Write-Host "  ❌ $failed tests failed" -ForegroundColor Red
        }
        else {
            $results += [PSCustomObject]@{
                Package = $package.Name
                Status = "⚠️  NO TESTS"
                Tests = "0 tests"
                Color = "Yellow"
            }
            Write-Host "  ⚠️  No tests found" -ForegroundColor Yellow
        }
    }
    catch {
        $results += [PSCustomObject]@{
            Package = $package.Name
            Status = "❌ ERROR"
            Tests = "Error: $_"
            Color = "Red"
        }
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

# Summary
Write-Host "`n" + ("="*80) -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host ("{0,-45} {1,-15} {2}" -f $result.Package, $result.Status, $result.Tests) -ForegroundColor $result.Color
}

$passCount = ($results | Where-Object { $_.Status -eq "✅ PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -like "*FAIL*" -or $_.Status -like "*ERROR*" }).Count

Write-Host "`n" + ("="*80) -ForegroundColor Cyan
Write-Host "Total: $passCount passed, $failCount failed out of $total packages" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Red" })
Write-Host ("="*80) -ForegroundColor Cyan

if ($failCount -gt 0) {
    exit 1
}
