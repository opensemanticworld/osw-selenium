# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OSW Selenium is a UI testing package for OpenSemanticWorld based on Selenium and Python. It is in early development (v0.0.1). The `migration/` directory contains legacy CodeceptJS tests and is gitignored.

## Commands

**Package manager:** uv

```bash
uv sync                          # Install dependencies
uv run pre-commit install        # Install pre-commit hooks
```

**Quality checks:**

```bash
make check                       # Run all quality tools (lock check, pre-commit, ty, deptry)
uv run pre-commit run -a         # Linting and formatting only
uv run ty check                  # Type checking
uv run deptry src                # Check for unused/missing dependencies
```

**Testing:**

```bash
make test                        # Run pytest with doctest-modules
uv run python -m pytest          # Run tests directly
uv run python -m pytest tests/test_foo.py          # Run a single test file
uv run python -m pytest tests/test_foo.py::test_fn # Run a single test function
tox                              # Run tests across Python 3.10-3.14
```

**Documentation:**

```bash
make docs                        # Build and serve docs with autobuild
make docs-test                   # Build docs with warnings-as-errors (-W)
```

**Build:**

```bash
make build                       # Build wheel file
```

## Architecture

- **Source code:** `src/osw_selenium/` — the installable package (hatchling build backend, `src` layout)
- **Tests:** `tests/` — pytest tests; doctests in source modules are also collected via `--doctest-modules`
- **Docs:** `docs/` — Sphinx documentation using Furo theme and MyST (Markdown)

## Code Style

- **Formatter/Linter:** Ruff (line length 120, target Python 3.10)
- **Type checker:** ty (configured to use the local `.venv`)
- **Pre-commit hooks** run Ruff check+format and standard file validators on commit
- `S101` (assert) is allowed in tests; `E501` (line length) and `E731` (lambda assignment) are globally ignored
- Use Google-style docstrings with type hints on all public functions
