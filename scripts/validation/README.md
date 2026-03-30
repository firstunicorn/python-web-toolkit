# Dependency Validation

This directory contains tools to validate dependency consistency across the monorepo.

## Overview

The validation system ensures:
1. Package names match their directory structure
2. No orphaned references exist in `poetry.lock`
3. Lock file stays in sync with `pyproject.toml`
4. All packages have valid metadata
5. Dependencies can be installed cleanly

## Files

- **`validate_packages.py`**: Standalone script for local validation
- **`.github/workflows/validate-dependencies.yml`**: CI workflow that runs on every push
- **`.pre-commit-config.yaml`**: Pre-commit hooks for local development

## Usage

### Manual Validation

Run the validation script locally:

```powershell
cd c:\coding\gridflow\python-web-toolkit
python scripts\validation\validate_packages.py
```

### Pre-commit Hooks (Recommended)

Install pre-commit hooks to validate before every commit:

```powershell
pip install pre-commit
pre-commit install
```

Now validation runs automatically on `git commit`. To run manually:

```powershell
pre-commit run --all-files
```

### CI Validation

The GitHub Actions workflow runs automatically on:
- Every push to `master` or `main`
- Every pull request

It performs comprehensive checks:
1. **Poetry validation**: `poetry check` and `poetry check --lock`
2. **Multi-package validation**: Validates each package's `pyproject.toml`
3. **Name/path consistency**: Ensures package names match directory structure
4. **Orphaned references**: Detects references to non-existent packages
5. **Lock file sync**: Regenerates lock file and checks for changes
6. **Clean installation**: Tests `poetry install --sync` from scratch

## Validation Checks

### Check 1: Name/Path Consistency

Ensures that dependency keys in root `pyproject.toml` match actual package names:

```toml
# Root pyproject.toml
[tool.poetry.dependencies]
gridflow-python-mediator = {path = "packages/gridflow-python-mediator", develop = true}
                           ↑                                             ↑
                           Must match name in package's pyproject.toml
```

**Catches:**
- Package renamed but root dependency not updated
- Typos in dependency names
- Missing packages

### Check 2: Orphaned References

Scans `poetry.lock` for references to `packages/*/` that no longer exist:

**Catches:**
- Old package names after renaming
- Deleted packages still in lock file
- Stale lock file after directory restructuring

### Check 3: Lock File Sync

Regenerates `poetry.lock` and compares with committed version:

**Catches:**
- Lock file not updated after `pyproject.toml` changes
- Version mismatches
- Missing dependencies

### Check 4: Clean Installation

Tests full dependency installation from scratch:

**Catches:**
- Runtime installation failures
- Missing system dependencies
- Circular dependencies
- Version conflicts

## What This Prevents

This validation would have caught:
- ✅ The `python-mediator` → `gridflow-python-mediator` rename issue
- ✅ Lock file referencing old package path
- ✅ Package metadata mismatches
- ✅ Missing or malformed `pyproject.toml` files

## Performance

- **Pre-commit hooks**: ~5-10 seconds (fast syntax checks only)
- **CI validation**: ~40-70 seconds (full validation + installation)

## Troubleshooting

### Lock file out of sync

```powershell
poetry lock
git add poetry.lock
git commit -m "fix: update poetry.lock"
```

### Orphaned references found

This usually means a package was renamed or deleted. Update the lock file:

```powershell
poetry lock
```

### Name/path mismatch

Ensure package name matches in both locations:

1. Root `pyproject.toml`: `[tool.poetry.dependencies]`
2. Package `pyproject.toml`: `[tool.poetry] name = "..."`

## Maintenance

To update Poetry version in pre-commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/python-poetry/poetry
    rev: '1.8.0'  # Update this version
```
