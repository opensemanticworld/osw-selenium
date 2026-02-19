# Getting Started

## Installation

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

:::{admonition} Requirements
:class: note

- Python 3.10 -- 3.14
- Chrome or Firefox installed on the host machine
- No Docker, webdriver-manager, or manual driver downloads needed --
  Selenium 4.6+ handles driver binaries automatically.
:::

## Basic Usage

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

## Pytest Fixtures

Use the provided fixtures in your test suite:

```python
def test_create_entry(json_editor):
    json_editor.open_create_instance_form(
        category="Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"
    )
    json_editor.fill_editor_field(schemapath="root.label.0.text", value="Test")
    json_editor.save_editor()
```

:::{admonition} Where do fixtures come from?
:class: tip

The fixtures (`osw_config`, `driver`, `logged_in_driver`, `login_page`,
`json_editor`) are defined in `tests/conftest.py`. Copy this file into your
project's `tests/` directory. See {doc}`concepts` for the fixture hierarchy.
:::

## Development Setup

Clone the repository and install the development environment:

```bash
git clone https://github.com/opensemanticworld/osw-selenium.git
cd osw-selenium
make install
```

Run quality checks and tests:

```bash
make check    # Linting, type checking, dependency validation
make test     # Unit tests + doctests
```

Build the documentation locally:

```bash
make docs-build   # Single build
make docs         # Build and serve with auto-reload
```
