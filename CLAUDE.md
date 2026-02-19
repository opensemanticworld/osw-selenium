# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Verification

After any code change, always run all three in order:

```bash
make check                       # Linting, type checking, dependency validation
make test                        # Unit tests + doctests
make docs-build                  # Build documentation (use 5s timeout for Bash tool)
```

`make check` must pass before `make test`. `make docs-build` catches broken autodoc references.
Use `timeout 5000` for `make docs-build` since sphinx can be slow.

After all three pass, update **CLAUDE.md** and **README.md** if the change affects:

- Package structure or new modules (update Architecture section in both files)
- New commands, config options, or environment variables
- New examples (update Examples section in README.md)
- New test categories or fixtures

## Commands

**Package manager:** uv

```bash
uv sync                          # Install dependencies
uv run pre-commit install        # Install pre-commit hooks
```

**Quality checks:**

```bash
make check                       # Run all quality tools (lock check, pre-commit, ty, deptry)
```

**Testing:**

```bash
make test                                              # Run pytest with doctest-modules
uv run python -m pytest tests/test_config.py           # Run a single test file
uv run python -m pytest tests/test_config.py::test_fn  # Run a single test function
tox                                                    # Run tests across Python 3.10-3.14
```

Integration tests require environment variables `MW_SITE_SERVER` and `MW_ADMIN_PASS`. They are auto-skipped when `MW_SITE_SERVER` is not set.

**Documentation:**

```bash
make docs-build                  # Build docs once (no server)
make docs                        # Build and serve docs with autobuild (long-running)
make docs-test                   # Build docs with warnings-as-errors (-W)
```

## Architecture

```text
src/osw_selenium/
├── config.py            # OSWConfig dataclass — reads MW_SITE_SERVER, MW_ADMIN_PASS, OSW_BROWSER, OSW_HEADLESS
├── driver.py            # create_driver() factory — Chrome/Firefox, headed/headless, no Docker needed
├── utils.py             # schema_path_to_name / name_to_schema_path conversions
└── pages/
    ├── base.py          # BasePage — wait, scroll, click, fill, JS execution
    ├── login.py         # LoginPage — login(), login_hidden()
    └── json_editor.py   # JsonEditorPage — editor-level state machine, form CRUD operations
```

- **Page Object pattern**: each OSL UI area is a class inheriting from `BasePage`
- **Editor-level state**: `JsonEditorPage` tracks nested inline editors via `_editor_level` / `_editor_id` — opening an inline form increments the level, saving/cancelling decrements it
- **Schema paths**: fields are addressed as dot-separated paths (e.g. `root.label.0.text`) and converted to form `name` attributes (`root[label][0][text]`) internally via `utils.py`
- **Fixtures**: `tests/conftest.py` provides session-scoped `osw_config`, `driver`, `logged_in_driver` and function-scoped page objects
- **Examples**: `examples/` contains runnable scripts; `tests/examples/` mirrors them with tests to ensure examples stay valid

## Code Style

- **Formatter/Linter:** Ruff (line length 120, target Python 3.10)
- **Type checker:** ty (configured to use the local `.venv`)
- **Pre-commit hooks** run Ruff check+format and standard file validators on commit
- `S101` (assert) is allowed in tests; `E501` (line length) and `E731` (lambda assignment) are globally ignored
- Use Google-style docstrings with type hints on all public functions
