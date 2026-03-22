"""Sphinx configuration for python-web-toolkit monorepo."""
import os
import sys

project = "python-web-toolkit"
copyright = "2026, GridFlow"
author = "GridFlow"

extensions = [
    "autoapi.extension",
    "myst_parser",
    "sphinx_copybutton",
]

autoapi_dirs = [
    f"../packages/{pkg}/src"
    for pkg in [
        "python-technical-primitives",
        "python-app-exceptions",
        "python-infrastructure-exceptions",
        "python-input-validation",
        "postgres-data-sanitizers",
        "pydantic-response-models",
        "python-cqrs-core",
        "python-mediator",
        "python-cqrs-dispatcher",
        "python-dto-mappers",
        "python-domain-events",
        "python-structlog-config",
        "fastapi-config-patterns",
        "fastapi-middleware-toolkit",
        "python-outbox-core",
        "sqlalchemy-async-session-factory",
        "sqlalchemy-async-repositories",
    ]
]
autoapi_type = "python"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_keep_files = True

myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

html_theme = "furo"
html_static_path = ["_static"]
templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

suppress_warnings = ["myst.header", "myst.xref_missing"]
