# OSW Selenium

:::{div} hero

**Selenium-based UI testing for OpenSemanticWorld**

Page objects, pytest fixtures, and helpers for login flows,
JSON editor forms, and wiki page interactions.

[![Release](https://img.shields.io/github/v/release/opensemanticworld/osw-selenium)](https://github.com/opensemanticworld/osw-selenium/releases)
[![License](https://img.shields.io/github/license/opensemanticworld/osw-selenium)](https://github.com/opensemanticworld/osw-selenium/blob/main/LICENSE)
[![Build status](https://img.shields.io/github/actions/workflow/status/opensemanticworld/osw-selenium/main.yml?branch=main)](https://github.com/opensemanticworld/osw-selenium/actions)
[![Python](https://img.shields.io/badge/python-3.10%E2%80%933.14-blue)](https://github.com/opensemanticworld/osw-selenium)

:::

---

## Install

::::{tab-set}

:::{tab-item} uv (recommended)
```bash
uv add osw-selenium
```
:::

:::{tab-item} pip
```bash
pip install osw-selenium
```
:::

::::

## Quick Start

:::{div} hero-code

```python
from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.login import LoginPage
from osw_selenium.pages.json_editor import JsonEditorPage

config = OSWConfig.from_env()
driver = create_driver(config)

LoginPage(driver, config).login()

editor = JsonEditorPage(driver, config)
editor.open_create_instance_form(category="Category:OSW0e7fab2262fb4427ad0fa454bc868a0d")
editor.fill_editor_field(schemapath="root.label.0.text", value="My entry")
editor.save_editor()

driver.quit()
```

:::

## Why OSW Selenium?

::::{grid} 2
:gutter: 3

:::{grid-item-card} Page Object Pattern
:class-header: sd-bg-light sd-font-weight-bold

Clean abstraction over raw Selenium calls. Each UI area (login, JSON editor)
is a self-contained class with typed methods and built-in waits.
:::

:::{grid-item-card} Multi-Browser Support
:class-header: sd-bg-light sd-font-weight-bold

Chrome and Firefox out of the box. Selenium 4.6+ auto-downloads drivers --
no webdriver-manager or Docker needed.
:::

:::{grid-item-card} Auto-Configuration
:class-header: sd-bg-light sd-font-weight-bold

`OSWConfig.from_env()` reads `MW_SITE_SERVER`, `MW_ADMIN_PASS`, `OSW_BROWSER`,
and `OSW_HEADLESS` from environment variables or `.env` files automatically.
:::

:::{grid-item-card} Pytest Fixtures
:class-header: sd-bg-light sd-font-weight-bold

Session-scoped driver, auto-login, and function-scoped page objects.
Drop `conftest.py` into your project and start writing tests immediately.
:::

:::{grid-item-card} Nested Editor State Machine
:class-header: sd-bg-light sd-font-weight-bold

`JsonEditorPage` tracks inline editor levels automatically --
open, fill, save, and assert across arbitrarily nested forms.
:::

:::{grid-item-card} Schema Path Addressing
:class-header: sd-bg-light sd-font-weight-bold

Address any form field with dot notation (`root.label.0.text`).
Automatic conversion to HTML `name` attributes handles bracket syntax internally.
:::

::::

## Learn More

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Getting Started
:link: getting-started
:link-type: doc

Installation, basic usage, and development setup.
:::

:::{grid-item-card} Configuration
:link: configuration
:link-type: doc

Environment variables, `.env` files, and CI pipeline setup.
:::

:::{grid-item-card} Architecture
:link: architecture
:link-type: doc

Class hierarchy, state machine, and design patterns.
:::

:::{grid-item-card} Concepts
:link: concepts
:link-type: doc

Page Object pattern, editor levels, and fixture design.
:::

:::{grid-item-card} Examples
:link: examples
:link-type: doc

Runnable scripts for common workflows.
:::

:::{grid-item-card} API Reference
:link: api/config
:link-type: doc

Complete auto-generated API documentation.
:::

::::

```{toctree}
:maxdepth: 3
:caption: Guide
:hidden:

getting-started
configuration
architecture
concepts
examples
```

```{toctree}
:maxdepth: 3
:caption: API Reference
:hidden:

api/config
api/driver
api/utils
api/pages-base
api/pages-login
api/pages-json-editor
```
