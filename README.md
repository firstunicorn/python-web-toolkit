# Python Web Toolkit

[![Tests](https://img.shields.io/badge/tests-331%20passing-brightgreen)](https://github.com/firstunicorn/python-web-toolkit/actions)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Comprehensive Python web development toolkit organized as a monorepo with 16 independent micro-libraries.

## Project Structure

This toolkit is designed to be integrated into your project as a **subfolder**:

```
your-project/
├── python-web-toolkit/          # This toolkit (clone/copy here)
│   ├── packages/
│   │   ├── python-app-exceptions/
│   │   ├── pydantic-response-models/
│   │   └── ... (14 more packages)
│   ├── pyproject.toml           # Workspace config
│   └── README.md
├── your-app/                    # Your application code
├── tests/
└── pyproject.toml               # Your project config
```

**Integration options:**
1. **Git submodule**: `git submodule add <repo-url> python-web-toolkit`
2. **Direct clone**: `git clone <repo-url> python-web-toolkit`
3. **Copy**: Download and place in your project

All installation commands assume `python-web-toolkit` is a **subfolder** in your project root.

**All commands below assume you're running from your project root** (where `python-web-toolkit/` folder is located).

## Architecture

This toolkit follows **microservices principles at the library level**:
- Each package is independently installable
- Packages are modularized as ≤100 lines per file (enforced by development rules)
- Zero or minimal dependencies per package
- Clear separation of concerns

### Dependency Architecture

**Primitives Layer** packages are strictly isolated with no cross-dependencies.

**Domain Layer** packages may depend on Primitives, but not on Application layer.

**Application Layer** packages may have lightweight dependencies:
- Application packages may import from domain and primitives packages
- CQRS/mediator packages integrate together
- All packages remain independently deployable

This layered architecture is enforced via Import Linter (see Architecture Validation section).

## Package Catalog

All packages are **v0.1.0** and independently installable.

### Core Primitives & Utilities (Layer: Primitives)
- **python-technical-primitives** - Text, datetime, and specification pattern utilities
  ```bash
  pip install python-technical-primitives
  ```
- **python-app-exceptions** - Application-level exception hierarchy
  ```bash
  pip install python-app-exceptions
  ```
- **python-infrastructure-exceptions** - Infrastructure exception types (database, cache, storage)
  ```bash
  pip install python-infrastructure-exceptions
  ```
- **python-input-validation** - Email and string validation/sanitization
  ```bash
  pip install python-input-validation
  ```
- **postgres-data-sanitizers** - PostgreSQL data sanitization (null chars, surrogates)
  ```bash
  pip install postgres-data-sanitizers
  ```
- **sqlalchemy-async-session-factory** - Async engine and session factories
  ```bash
  pip install sqlalchemy-async-session-factory
  ```
- **python-structlog-config** - Structured logging configuration presets (dev/prod/test)
  ```bash
  pip install python-structlog-config
  ```

### CQRS & Mediator Pattern (Layer: Domain)
- **python-cqrs-core** - CQRS interfaces (ICommand, IQuery, BaseCommand, BaseQuery)
  ```bash
  pip install python-cqrs-core
  ```
- **python-mediator** - Generic mediator with pipeline behaviors
  ```bash
  pip install python-mediator
  ```
- **python-cqrs-dispatcher** - CQRS dispatcher integrating commands/queries with mediator
  ```bash
  pip install python-cqrs-dispatcher
  ```

### Data & Mapping (Layer: Domain)
- **python-dto-mappers** - Auto-mapping engine and decorators for DTO transformations
  ```bash
  pip install python-dto-mappers
  ```
- **pydantic-response-models** - Standard API response DTOs using Pydantic (framework-agnostic)
  ```bash
  pip install pydantic-response-models
  ```

### Database & Repository Pattern (Layer: Application)
- **sqlalchemy-async-repositories** - Async repository pattern implementation
  ```bash
  pip install sqlalchemy-async-repositories
  ```

### FastAPI Extensions (Layer: Application)
- **fastapi-config-patterns** - Reusable Pydantic settings classes
  ```bash
  pip install fastapi-config-patterns
  ```
- **fastapi-middleware-toolkit** - FastAPI middleware setup (CORS, error handlers, lifespan)
  ```bash
  pip install fastapi-middleware-toolkit
  ```

### Event-Driven / Outbox Pattern (Layer: Domain)
- **python-outbox-core** - Transactional outbox pattern with CloudEvents formatters
  ```bash
  pip install python-outbox-core
  ```

## Quick Start

### Option 1: Install Entire Workspace (Recommended for Development)

```powershell
# From python-web-toolkit root
poetry install
```

This installs all packages in editable mode with cross-references working automatically.

**Benefits:**
- ✅ One command installs everything
- ✅ Cross-package imports work automatically
- ✅ Shared virtual environment
- ✅ Consistent dependency resolution

### Option 2: Install Individual Packages

```powershell
# Install specific package
cd packages/python-cqrs-core
poetry install

# Run tests
poetry run pytest -v
```

**Use when:** Working on a single package in isolation.

**⚠️ Note:** Some packages have cross-dependencies within the monorepo:
- `python-cqrs-dispatcher` requires `python-cqrs-core` + `python-mediator`
- `sqlalchemy-async-repositories` may require specific Python constraints

For packages with cross-dependencies, use **Option 1 (Workspace)** instead.

### Option 3: Bulk Install with Script (Recommended for CI/CD)

```powershell
# From python-web-toolkit root
.\scripts\install-all.ps1
```

**Benefits:**
- ✅ Progress tracking per package
- ✅ Error handling and reporting
- ✅ Colored output for quick scanning
- ✅ CI/CD friendly

### Option 4: Quick One-Liner (For Experienced Developers)

```powershell
# From python-web-toolkit root
Get-ChildItem packages -Directory | ForEach-Object {
    cd $_.FullName; poetry install --quiet
}
```

**Use when:** You need a quick manual install without script overhead.

### Option 5: Individual pip Installs (For Custom Setups)

```bash
# Install all packages in editable mode with pip
# Run from your project root (where python-web-toolkit folder is located)
pip install -e ./python-web-toolkit/packages/python-app-exceptions
pip install -e ./python-web-toolkit/packages/pydantic-response-models
pip install -e ./python-web-toolkit/packages/sqlalchemy-async-repositories
pip install -e ./python-web-toolkit/packages/python-technical-primitives
pip install -e ./python-web-toolkit/packages/postgres-data-sanitizers
pip install -e ./python-web-toolkit/packages/python-input-validation
pip install -e ./python-web-toolkit/packages/fastapi-middleware-toolkit
pip install -e ./python-web-toolkit/packages/fastapi-config-patterns
pip install -e ./python-web-toolkit/packages/sqlalchemy-async-session-factory
pip install -e ./python-web-toolkit/packages/python-structlog-config
pip install -e ./python-web-toolkit/packages/python-infrastructure-exceptions
pip install -e ./python-web-toolkit/packages/python-dto-mappers
pip install -e ./python-web-toolkit/packages/python-cqrs-core
pip install -e ./python-web-toolkit/packages/python-mediator
pip install -e ./python-web-toolkit/packages/python-cqrs-dispatcher
pip install -e ./python-web-toolkit/packages/python-outbox-core
```

This is **LOCAL installation** from your filesystem, **NOT from PyPI**.

## What `pip install -e` Does:

**`-e`** = **"editable mode"** (also called "development mode")

When you run:
```bash
pip install -e ./python-web-toolkit/packages/python-app-exceptions
```

It means:
1. ✅ Install the package from **LOCAL filesystem** (the `./python-web-toolkit/packages/...` path)
2. ✅ Install in **editable mode** - changes to source code are immediately active (no need to reinstall)
3. ❌ Does **NOT** download from PyPI

## Why Use Editable Mode?

Perfect for **monorepo development**:
- You edit `python-app-exceptions/src/...` files
- Changes are instantly available to other packages or projects
- No need to rebuild/reinstall after every change

## Install from PyPI

If you need these packages **from PyPI**, you'd install normally:
```bash
pip install python-app-exceptions  # Downloads from pypi.org
```

**When to use `-e .`:** You need fine-grained control over which packages to install with pip.

**📝 Note about `-e` flag:**
- `-e` = **editable/development mode** - installs from **LOCAL filesystem**, NOT from PyPI
- Source code changes take effect immediately (no reinstall needed)
- Paths are relative to your project structure
- Perfect for monorepo development where packages are not yet published or custom modifications required

## Development

### Running All Tests

**Option 1: Workspace (Fastest)**
```powershell
# From python-web-toolkit root
poetry run pytest
```

**Option 2: Test Script with Summary (CI/CD)**
```powershell
.\scripts\test-all.ps1
```
Provides detailed summary with pass/fail counts per package.

**Option 3: Quick One-Liner (Manual)**
```powershell
Get-ChildItem packages -Directory | ForEach-Object {
    cd $_.FullName; poetry run pytest -v --tb=short
}
```

**Option 4: Single Package**
```powershell
cd packages/python-cqrs-core
poetry run pytest -v
```

**Option 5: All Packages with Import Mode (Advanced)**
```bash
# Test all micro-library packages (from your project root)
poetry run pytest python-web-toolkit/packages/ --import-mode=importlib -v
```

**Option 6: Save Test Output to Log**
```powershell
# Save detailed test output (from your project root)
poetry run pytest python-web-toolkit/packages/ --import-mode=importlib -v 2>&1 | Tee-Object -FilePath tests/logs/micro_libs_all.txt
```

### Code Quality Standards

- **Architecture**: OOP, DRY, SOLID principles, Layered Architecture
- **Line limit**: 100 lines per file (absolute maximum: 120)
- **Organization**: Split into sub-modules when approaching limit
- **Test coverage**: Comprehensive unit + property-based tests
- **Import rules**: Enforced via Import Linter (see Architecture section)

### Architecture Validation

**Import Linter** enforces architectural boundaries (122 files, 151 dependencies analyzed):

```powershell
# Check import rules
.\scripts\check-architecture.ps1
# Or directly: poetry run lint-imports

# Run with tests
poetry run pytest && poetry run lint-imports
```

**3 Architectural Contracts (All Passing ✓):**

1. **Primitives Layer Cannot Import Domain/Application** - Bottom layer stays isolated
   - `python-technical-primitives`, `python-app-exceptions`, `python-infrastructure-exceptions`
   - ✗ Cannot import: CQRS, mediator, repositories, FastAPI, DTOs

2. **Domain Layer Cannot Import Application** - Mid layer depends only on primitives
   - `python-cqrs-core`, `python-mediator`, `pydantic-response-models`, `python-dto-mappers`
   - ✗ Cannot import: `python-cqrs-dispatcher`, repositories, FastAPI middleware

3. **Core Components Independence** - Prevents circular dependencies
   - `python-cqrs-core` and `python-mediator` must not import each other

**Layer Hierarchy:**

| Layer | Position | Packages | Import Rules |
|-------|----------|----------|--------------|
| **Application** | Top | `python-cqrs-dispatcher`<br>`sqlalchemy-async-repositories`<br>`fastapi-middleware-toolkit`<br>`fastapi-config-patterns` | ✅ Can import from any layer |
| **Domain** | Middle | `python-cqrs-core`<br>`python-mediator`<br>`pydantic-response-models`<br>`python-dto-mappers`<br>`python-input-validation`<br>`python-outbox-core` | ✅ Can import primitives<br>❌ Cannot import application |
| **Primitives** | Bottom | `python-technical-primitives`<br>`python-app-exceptions`<br>`python-infrastructure-exceptions`<br>`postgres-data-sanitizers`<br>`sqlalchemy-async-session-factory`<br>`python-structlog-config` | ❌ Cannot import domain/application<br>(Fully isolated foundation) |

**Text Summary:**
- **Primitives** (bottom): `python-technical-primitives`, exceptions → Cannot import domain/application
- **Domain** (middle): `python-cqrs-core`, `python-mediator`, DTOs → Cannot import application
- **Application** (top): `python-cqrs-dispatcher`, repositories, FastAPI → Can import anything

### Adding a New Package

1. Create package structure:
   ```powershell
   cd packages
   poetry new my-new-package
   ```

2. Add to workspace `pyproject.toml`:
   ```toml
   my-new-package = {path = "packages/my-new-package", develop = true}
   ```

3. Install workspace:
   ```bash
   poetry install
   ```

## Documentation

- [Examples Overview](examples/README.md) - All 15 examples organized by use case
- [Quick Start Guide](examples/QUICK_START.md) - 5 essential examples to get started
- [Domain Layer Examples](examples/domain/) - Business logic and data patterns
- [Infrastructure Examples](examples/infrastructure/) - APIs, database, CQRS, messaging

## Publishing to PyPI

**First time setup:**
1. Create PyPI account: https://pypi.org/account/register/
2. Generate API token: https://pypi.org/manage/account/token/
3. Configure `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```
4. Install tools: `pip install --upgrade build twine`

**Publishing new version:**
```powershell
# 1. Bump version in pyproject.toml (e.g., 0.1.0 → 0.1.1)
# 2. Build all packages
.\scripts\build-all.ps1

# 3. Test on Test PyPI first (recommended)
.\scripts\publish-test.ps1

# 4. Publish to production PyPI
.\scripts\publish-prod.ps1
```

**Note:** Packages must be published in dependency order (Layer 1 → 2 → 3). Scripts handle this automatically.

## License

MIT
