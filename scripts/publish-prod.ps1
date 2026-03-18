# Publish All Packages to Production PyPI
# Run from python-web-toolkit root
#
# Usage: .\scripts\publish-prod.ps1
#
# Prerequisites:
# - Build tools installed: pip install build twine
# - ~/.pypirc configured with Production PyPI token
# - Packages already built (run build-all.ps1 first)
# - Tested on Test PyPI first (run publish-test.ps1)
#
# WARNING: This publishes to PRODUCTION PyPI and cannot be undone
# Requires manual confirmation before proceeding

Write-Host "WARNING: Publishing to PRODUCTION PyPI" -ForegroundColor Red
Write-Host "This action cannot be undone!" -ForegroundColor Red
$confirmation = Read-Host "Type 'YES' to continue"

if ($confirmation -ne 'YES') {
    Write-Host "Aborted." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nPublishing all packages to Production PyPI..." -ForegroundColor Cyan
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
                Write-Host "  Uploading to PRODUCTION..." -ForegroundColor Gray
                python -m twine upload dist/* 2>&1 | Out-Null
                
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
