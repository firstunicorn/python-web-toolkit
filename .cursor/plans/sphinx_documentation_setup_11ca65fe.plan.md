---
name: Sphinx documentation setup
overview: "Set up Sphinx documentation with sphinx-autoapi for the 17-package monorepo, hosted on Read the Docs. The plan uses a multi-stage approach: first gather full context from all package source files, then generate hand-written guides + auto-generated API reference."
todos:
  - id: ctx-batch-1
    content: "Stage 1 batch 1: read all __init__.py exports + pyproject.toml metadata (17 packages)"
    status: completed
  - id: ctx-batch-2
    content: "Stage 1 batch 2: read all 134 source files docstrings and signatures (parallel agents by package group)"
    status: completed
  - id: ctx-batch-3
    content: "Stage 1 batch 3: read ALL existing docs -- cqrs-core/docs (4), sqlalchemy-repos (4), outbox-core/detailed-docs (5), EXCEPTION_COMPARISON, all 17 READMEs"
    status: completed
  - id: ctx-batch-4
    content: "Stage 1 batch 4: read root README.md (829 lines) + import-linter contracts in pyproject.toml"
    status: completed
  - id: scaffold
    content: "Stage 2: scaffold -- add docs deps, create docs/conf.py, Makefile, .readthedocs.yaml, update .gitignore"
    status: completed
  - id: guides-rich
    content: "Stage 3a: create thin wrapper pages for 3 rich-docs packages (cqrs-core, sqlalchemy-repos, outbox-core) that toctree-include existing .md"
    status: completed
  - id: guides-new
    content: "Stage 3b: create new guide pages for 14 README-only packages (content from README + docstrings)"
    status: completed
  - id: guides-top
    content: "Stage 3c: create top-level pages -- index.rst, quickstart.md, architecture.md, exception-comparison.md"
    status: completed
  - id: compat-fixes
    content: "Stage 3d: fix existing .md files for myst-parser compatibility (heading levels, emoji, HTML tags)"
    status: completed
  - id: build-verify
    content: "Stage 4: build and verify -- run sphinx build, fix warnings, verify autoapi + toctree rendering"
    status: completed
isProject: false
---

# Sphinx documentation for python-web-toolkit monorepo

## Current state

- No Sphinx setup exists anywhere in the repo
- No docs dependencies in [pyproject.toml](pyproject.toml)
- The repo uses Poetry (root) + setuptools (per-package builds)
- 17 packages, 134 source files total, all under `packages/*/src/`
- Inter-package deps: only `python-cqrs-dispatcher` depends on `python-cqrs-core` + `python-mediator`

### Existing markdown documentation (MUST be reused, not duplicated)

**Packages with rich docs (3):**

- **python-cqrs-core** -- `packages/python-cqrs-core/docs/` (4 files):
  - `usage-guide.md` (298 lines, full examples for commands/queries/pagination/tracing)
  - `api-reference.md` (interfaces, base classes)
  - `observability.md` (OTel/Sentry/Prometheus integration)
  - `why-use-base-classes.md` (design rationale)
- **sqlalchemy-async-repositories** -- root-level docs (4 files):
  - `ARCHITECTURE.md` (design patterns, interactions)
  - `HYBRID_IMPLEMENTATION_SUMMARY.md` (hybrid approach details)
  - `REFACTORING_SUMMARY_FACTORY_PATTERN.md` (factory pattern)
  - `MISSED FROM ARCHITECTURE.md` (supplementary architecture)
- **python-outbox-core** -- `QUICKREF.md` + `detailed-docs/` (5 files):
  - `QUICKREF.md` (quick reference card)
  - `detailed-docs/API_REFERENCE.md` (full API reference)
  - `detailed-docs/IMPLEMENTATION_GUIDE.md` (implementation checklist)
  - `detailed-docs/faq/OUTBOX_VS_TASK_QUEUES.md` (comparison)
  - `detailed-docs/faq/SERIALIZATION_NOTES.md` (Pydantic/FastStream)

**Cross-package doc (1):**

- `packages/EXCEPTION_LIBRARIES_COMPARISON.md` (python-app-exceptions vs python-infrastructure-exceptions)

**README only (14 packages):** each has a `README.md` with description, installation, basic usage.

### Strategy for existing docs

- myst-parser includes existing `.md` files directly via toctree -- NO copying/duplicating
- Sphinx toctree entries point to relative paths into `packages/` using `../packages/...`
- Each package's guide page in `docs/packages/` will toctree-include its existing docs as sub-pages
- Minor edits to existing `.md` files only if needed for myst compatibility (e.g., adding myst front-matter or fixing heading levels)

## Architecture

```
docs/
├── conf.py                    # sphinx config (autoapi, myst, furo theme)
├── index.rst                  # root toctree
├── installation.rst           # pip install instructions (TestPyPI/PyPI)
├── quickstart.md              # getting started guide (myst)
├── architecture.md            # layer diagram, dependency graph
├── exception-comparison.md    # symlink/include of packages/EXCEPTION_LIBRARIES_COMPARISON.md
├── packages/                  # per-package guide pages (thin wrappers)
│   ├── index.rst              # package listing toctree
│   ├── python-app-exceptions.md          # new guide (README-only pkg)
│   ├── python-technical-primitives.md    # new guide (README-only pkg)
│   ├── python-cqrs-core.md              # toctree wrapper -> includes existing docs/
│   ├── sqlalchemy-async-repositories.md  # toctree wrapper -> includes existing .md files
│   ├── python-outbox-core.md             # toctree wrapper -> includes existing detailed-docs/
│   └── ... (one .md per package)
├── _static/
└── _templates/
```

**Key: packages WITH existing docs get thin wrapper pages that toctree-include their existing .md files.
Packages WITHOUT existing docs get a new guide page with content extracted from README + docstrings.**

Auto-generated API reference lands in `docs/autoapi/` (gitignored, built at build time).

## Key technical decisions

- **sphinx-autoapi** (not sphinx.ext.autodoc): works without importing packages, ideal for monorepo where not all deps are installed. `autoapi_dirs` will point to all 17 `packages/*/src/` directories
- **myst-parser**: allows writing guides in `.md` alongside `.rst` for toctrees
- **furo** theme: clean, modern, RTD-compatible
- **readthedocs.yaml v2**: config for RTD builds with Poetry

## Stage 1: context gathering from code

Before writing any documentation files, systematically grep/read in batches:

**Batch 1 -- public API surface (already partially gathered):**

1. Every `__init__.py` public API exports (17 packages -- done in planning)
2. Each package's `pyproject.toml` for name, version, description, dependencies

**Batch 2 -- docstrings and signatures (134 source files, parallel agents):**
3. All source modules' docstrings and class/function signatures grouped by package
4. Focus on: class docstrings, method signatures with type hints, module-level docstrings

**Batch 3 -- existing documentation (MUST read before writing anything):**
5. All 4 files in `packages/python-cqrs-core/docs/` (full read)
6. All 4 architecture docs in `packages/sqlalchemy-async-repositories/` (full read)
7. All files in `packages/python-outbox-core/detailed-docs/` + `QUICKREF.md` (full read)
8. `packages/EXCEPTION_LIBRARIES_COMPARISON.md` (full read)
9. Every package `README.md` (17 files -- extract usage examples)

**Batch 4 -- architecture context:**
10. The root [README.md](README.md) before/after examples (all 829 lines)
11. The import-linter contracts in [pyproject.toml](pyproject.toml) (layer boundaries)

This context feeds into:

- Stage 2: knowing which existing .md files need myst compatibility fixes
- Stage 3: writing new guide pages for README-only packages
- Stage 3: writing accurate quickstart.md and architecture.md

## Stage 2: scaffold sphinx infrastructure

1. Add docs dependencies to root `pyproject.toml` under `[tool.poetry.group.docs.dependencies]`:
  - `sphinx`, `sphinx-autoapi`, `myst-parser`, `furo`, `sphinx-copybutton`
2. Create `docs/conf.py` with:

```python
   extensions = ["autoapi.extension", "myst_parser", "sphinx_copybutton"]
   autoapi_dirs = [
       "../packages/python-technical-primitives/src",
       "../packages/python-app-exceptions/src",
       # ... all 17 packages
   ]
   autoapi_type = "python"
   autoapi_options = ["members", "undoc-members", "show-inheritance", "show-module-summary"]
   html_theme = "furo"
   myst_enable_extensions = ["colon_fence", "deflist"]


```

1. Create `docs/Makefile` and `docs/make.bat` (standard sphinx)
2. Create `.readthedocs.yaml` at repo root:

```yaml
   version: 2
   build:
     os: "latest"
     tools:
       python: "3.10"
   sphinx:
     configuration: docs/conf.py
   python:
     install:
       - method: pip
         path: .
         extra_requirements:
           - docs


```

1. Add `docs/autoapi/` and `docs/_build/` to [.gitignore](.gitignore)

## Stage 3: hand-written guides (context dump)

### For packages WITH existing docs (3 packages) -- thin wrapper approach:

Create `docs/packages/{pkg-name}.md` as a **toctree wrapper** that:

- Has a short intro paragraph (description from pyproject.toml)
- Installation command
- Links to autoapi-generated API reference
- Uses myst `toctree` directive to include existing docs as sub-pages:

```md
# python-cqrs-core

CQRS interfaces and base classes with tracing support.

## Installation
pip install python-cqrs-core

```{toctree}
:maxdepth: 2

../../packages/python-cqrs-core/docs/usage-guide
../../packages/python-cqrs-core/docs/api-reference
../../packages/python-cqrs-core/docs/observability
../../packages/python-cqrs-core/docs/why-use-base-classes
```

Same pattern for `sqlalchemy-async-repositories` (4 docs) and `python-outbox-core` (QUICKREF + detailed-docs/).

### For packages WITHOUT existing docs (14 packages) -- new guide pages:

Create `docs/packages/{pkg-name}.md` containing:

- One-line description (from pyproject.toml)
- Installation command
- Public API summary table (class/function, one-liner)
- Usage examples (extracted from that package's README.md before/after sections + docstrings)
- Cross-links to auto-generated API ref via autoapi roles

### Top-level pages:

- `index.rst`: main toctree linking to quickstart, architecture, packages, exception-comparison, API reference
- `quickstart.md`: install instructions, minimal working example
- `architecture.md`: layer diagram (primitives -> domain -> application -> infrastructure), import-linter contracts, inter-package dependency graph
- `exception-comparison.md`: include of `packages/EXCEPTION_LIBRARIES_COMPARISON.md`

### Existing .md compatibility fixes (if needed):

Some existing docs may need minor adjustments for myst-parser:

- Heading level consistency (ensure no duplicate H1 within a toctree)
- GitHub-flavored markdown features that myst doesn't support (e.g., `<details>` tags may need `{raw} html` directive)
- Remove emoji shortcuts if they break rendering

## Stage 4: build and verify

1. `cd docs && make html` -- verify no warnings
2. Check auto-generated API pages render correctly for all 17 packages
3. Verify cross-references between hand-written guides and autoapi pages
4. Test RTD build locally with `readthedocs-build`

## File size discipline

All files under 75 lines. If a package guide exceeds this, split into `docs/packages/{pkg-name}/index.md` + sub-pages.