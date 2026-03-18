#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run tests for all packages with combined coverage report
.DESCRIPTION
    Iterates through all packages, runs pytest with coverage from root,
    and generates a combined HTML coverage report.
.PARAMETER Thorough
    Use thorough Hypothesis profile (1000 examples instead of 100)
.EXAMPLE
    .\test-all-with-coverage.ps1
    .\test-all-with-coverage.ps1 -Thorough
#>

param(
    [switch]$Thorough
)

$ErrorActionPreference = "Continue"

$scriptDir = $PSScriptRoot
$rootDir = Split-Path (Split-Path $scriptDir -Parent) -Parent
$packagesDir = Join-Path $rootDir "python-web-toolkit\packages"
$packages = Get-ChildItem $packagesDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "tests")
}

# Setup coverage
$coverageFile = Join-Path $packagesDir ".coverage"
if (Test-Path $coverageFile) {
    Remove-Item $coverageFile -Force
}
if (Test-Path "$coverageFile.*") {
    Remove-Item "$coverageFile.*" -Force
}

$env:COVERAGE_FILE = $coverageFile

Write-Host "`n==================================================================================================" -ForegroundColor Cyan
Write-Host "TESTING PYTHON WEB TOOLKIT PACKAGES WITH COVERAGE" -ForegroundColor Cyan
Write-Host "==================================================================================================" -ForegroundColor Cyan
Write-Host ""

# Set Hypothesis profile
$hypothesisProfile = if ($Thorough) { "thorough" } else { "default" }
$maxExamples = if ($Thorough) { "1000" } else { "100" }
Write-Host "Hypothesis profile: $hypothesisProfile ($maxExamples examples)" -ForegroundColor Yellow
Write-Host ""

$results = @()
$total = $packages.Count
$current = 0

foreach ($package in $packages) {
    $current++
    
    Write-Host "`n=== [$current/$total] Testing $($package.Name) ===" -ForegroundColor Cyan
    
    Push-Location $rootDir
    
    try {
        $testDir = Join-Path $package.FullName "tests"
        $srcDir = Join-Path $package.FullName "src"
        
        # Build pytest command - run from root with absolute paths
        $pytestArgs = @(
            $testDir,
            "-p", "thorough_profile",
            "--cov=$srcDir",
            "--cov-append",
            "--cov-report=term-missing:skip-covered"
        )
        
        Write-Host "Running pytest for $($package.Name)..." -ForegroundColor DarkGray
        Write-Host ""
        
        # We must change directory to the root where poetry is installed
        Push-Location $rootDir
        
        # Run pytest with PYTHONPATH set to script directory so it finds our plugin
        $env:PYTHONPATH = $scriptDir
        # Tell the plugin to switch to thorough profile if requested
        if ($Thorough) { $env:THOROUGH_TESTS = "1" }
        
        # Run pytest and show output in real-time
        & poetry run pytest @pytestArgs
        $exitCode = $LASTEXITCODE
        
        $env:PYTHONPATH = ""
        
        Pop-Location
        
        Write-Host ""
        
        # Check exit code
        if ($exitCode -eq 0) {
            $status = "PASS"
            $color = "Green"
            Write-Host "  [PASS] $($package.Name)" -ForegroundColor Green
        }
        elseif ($exitCode -eq 5) {
            $status = "NO TESTS"
            $color = "Yellow"
            Write-Host "  [SKIP] $($package.Name) - No tests found" -ForegroundColor Yellow
        }
        else {
            $status = "FAIL"
            $color = "Red"
            Write-Host "  [FAIL] $($package.Name) - Exit Code: $exitCode" -ForegroundColor Red
        }

        $results += [PSCustomObject]@{
            Package = $package.Name
            Status = $status
            Color = $color
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

# Generate combined HTML coverage report
Write-Host '\n=== Generating combined coverage report ===' -ForegroundColor Cyan
Push-Location $rootDir
poetry run coverage html -d 'python-web-toolkit\packages\htmlcov-libraries' 2>&1 | Out-Null
$coveragePath = Join-Path (Join-Path $packagesDir 'htmlcov-libraries') 'index.html'
Pop-Location

Write-Host "`n===================================================================================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "===================================================================================================" -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host ("{0,-50} {1}" -f $result.Package, $result.Status) -ForegroundColor $result.Color
}

$passCount = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$skipCount = ($results | Where-Object { $_.Status -eq "NO TESTS" }).Count

Write-Host "`n===================================================================================================" -ForegroundColor Cyan
Write-Host "Total: $passCount passed, $failCount failed, $skipCount skipped out of $total packages" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Red" })
Write-Host 'Coverage report: python-web-toolkit\packages\htmlcov-libraries\index.html' -ForegroundColor Cyan
Write-Host "===================================================================================================" -ForegroundColor Cyan

# Cleanup
if (Test-Path $env:COVERAGE_FILE) {
    Remove-Item $env:COVERAGE_FILE -ErrorAction SilentlyContinue
}
Get-ChildItem -Path $packagesDir -Filter '.coverage.*' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

if ($failCount -gt 0) {
    exit 1
}
