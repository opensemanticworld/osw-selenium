# OSW Selenium <!-- omit in toc -->

[![Release](https://img.shields.io/github/v/release/opensemanticworld/osw-selenium)](https://github.com/opensemanticworld/osw-selenium/releases)
[![Build status](https://img.shields.io/github/actions/workflow/status/opensemanticworld/osw-selenium/main.yml?branch=main)](https://github.com/opensemanticworld/osw-selenium/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/opensemanticworld/osw-selenium/branch/main/graph/badge.svg)](https://codecov.io/gh/opensemanticworld/osw-selenium)
[![Commit activity](https://img.shields.io/github/commit-activity/m/opensemanticworld/osw-selenium)](https://github.com/opensemanticworld/osw-selenium/graphs/commit-activity)
[![License](https://img.shields.io/github/license/opensemanticworld/osw-selenium)](https://github.com/opensemanticworld/osw-selenium/blob/main/LICENSE)

Reusable Python library for UI testing [OpenSemanticLab](https://github.com/OpenSemanticLab) instances using Selenium. Provides page objects, pytest fixtures, and helpers for login flows, JSON editor forms, and wiki page interactions.

- **GitHub repository**: <https://github.com/opensemanticworld/osw-selenium/>
- **Documentation**: <https://opensemanticworld.github.io/osw-selenium/>

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Examples](#examples)

## Installation

Using `uv` (recommended):

```bash
uv add osw-selenium
```

Using `pip`:

```bash
pip install osw-selenium
```

## Configuration

Set these environment variables (or use a `.env` file with the `dotenv` extra):

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `MW_SITE_SERVER` | Yes | `http://localhost` | Base URL of the OSL/MediaWiki instance |
| `MW_ADMIN_PASS` | Yes | — | Admin password |
| `OSW_BROWSER` | No | `chrome` | `chrome` or `firefox` |
| `OSW_HEADLESS` | No | `false` | `true` for headless mode (CI pipelines) |

See [`.env.example`](.env.example) for a template.

## Quick Start

```python
from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.login import LoginPage
from osw_selenium.pages.json_editor import JsonEditorPage

config = OSWConfig.from_env()
driver = create_driver(config)

# Login
login_page = LoginPage(driver, config)
login_page.login()

# Create an ELN entry
editor = JsonEditorPage(driver, config)
editor.open_create_instance_form(category="Category:OSW0e7fab2262fb4427ad0fa454bc868a0d")
editor.fill_editor_field(schemapath="root.label.0.text", value="My entry")
editor.save_editor()

driver.quit()
```

Or use the provided pytest fixtures in your test suite:

```python
def test_create_entry(json_editor):
    json_editor.open_create_instance_form(
        category="Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"
    )
    json_editor.fill_editor_field(schemapath="root.label.0.text", value="Test")
    json_editor.save_editor()
```

## Examples

The [`examples/`](examples/) directory contains runnable scripts demonstrating common use cases:

| Example | Description |
| --- | --- |
| [`basic_config.py`](examples/basic_config.py) | Configure `OSWConfig` from env vars or explicit values |
| [`schema_path_utils.py`](examples/schema_path_utils.py) | Convert between dot paths and bracket-style field names |
| [`login_and_verify.py`](examples/login_and_verify.py) | Log in and verify the main page loads |
| [`create_eln_entry.py`](examples/create_eln_entry.py) | Create an ELN entry with inline organization and person |

Each example has a corresponding test in [`tests/examples/`](tests/examples/) to ensure examples stay valid.
