# Publish All Packages to Test PyPI
# Run from python-web-toolkit root
#
# Usage: .\scripts\publish-test.ps1
#
# Prerequisites:
# - Build tools installed: pip install build twine
# - ~/.pypirc configured with Test PyPI token
# - Packages already built (run build-all.ps1 first)
#
# This script publishes in dependency order to Test PyPI for validation
# Test installation: pip install --index-url https://test.pypi.org/simple/ <package-name>

Write-Host "Publishing all packages to Test PyPI..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

$packages = @(
    "python-technical-primitives",
    "python-app-exceptions",
    "python-infrastructure-exceptions",
    "python-input-validation",
    "postgres-data-sanitizers",
    "sqlalchemy-async-session-factory",
    "python-structlog-config",
    "python-cqrs-core",
    "python-mediator",
    "pydantic-response-models",
    "python-dto-mappers",
    "python-domain-events",
    "python-outbox-core",
    "python-cqrs-dispatcher",
    "sqlalchemy-async-repositories",
    "fastapi-config-patterns",
    "fastapi-middleware-toolkit"
)

$success = 0
$failed = 0
$skipped = 0

foreach ($pkg in $packages) {
    Write-Host "`n[$($packages.IndexOf($pkg) + 1)/$($packages.Count)] Publishing $pkg..." -ForegroundColor Yellow
    
    $pkgPath = "packages\$pkg"
    if (-not (Test-Path $pkgPath)) {
        Write-Host "  [SKIP] Package directory not found" -ForegroundColor Magenta
        $skipped++
        continue
    }
    
    Push-Location $pkgPath
    
    try {
        Write-Host "  Building..." -ForegroundColor Gray
        python -m build --wheel --sdist 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Checking..." -ForegroundColor Gray
            python -m twine check dist/* 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  Uploading..." -ForegroundColor Gray
                python -m twine upload --repository testpypi dist/* 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "  [OK] Published successfully" -ForegroundColor Green
                    $success++
                } else {
                    Write-Host "  [FAIL] Upload failed" -ForegroundColor Red
                    $failed++
                }
            } else {
                Write-Host "  [FAIL] Package check failed" -ForegroundColor Red
                $failed++
            }
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
Write-Host "  Skipped: $skipped" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Cyan
