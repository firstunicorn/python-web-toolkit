# Build All Packages
# Run from python-web-toolkit root
#
# Usage: .\scripts\build-all.ps1
#
# This script:
# - Cleans existing dist/ folders
# - Builds wheel + source distributions for all packages
# - Reports success/failure summary
#
# Output: packages/*/dist/*.whl and *.tar.gz files

Write-Host "Building all packages..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

$packages = Get-ChildItem packages -Directory

$success = 0
$failed = 0

foreach ($pkg in $packages) {
    Write-Host "`n[$($packages.IndexOf($pkg) + 1)/$($packages.Count)] Building $($pkg.Name)..." -ForegroundColor Yellow
    
    Push-Location $pkg.FullName
    
    try {
        if (Test-Path "dist") {
            Remove-Item "dist" -Recurse -Force
        }
        
        python -m build --wheel --sdist 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Built successfully" -ForegroundColor Green
            $success++
        } else {
            Write-Host "  [FAIL] Build failed" -ForegroundColor Red
            $failed++
        }
    }
    catch {
        Write-Host "  [ERROR] $_" -ForegroundColor Red
        $failed++
    }
    finally {
        Pop-Location
    }
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Success: $success" -ForegroundColor Green
Write-Host "  Failed:  $failed" -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Cyan

if ($success -gt 0) {
    Write-Host "`nBuilt packages are in packages/*/dist/" -ForegroundColor Cyan
}
