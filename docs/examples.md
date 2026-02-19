# Examples

The [`examples/`](https://github.com/opensemanticworld/osw-selenium/tree/main/examples) directory contains runnable scripts demonstrating common use cases.

## Basic Configuration

Configure `OSWConfig` from environment variables or explicit values.

```python
from osw_selenium.config import OSWConfig

# From environment variables (and .env file)
config = OSWConfig.from_env()
print(f"Base URL: {config.base_url}")
print(f"Browser:  {config.browser}")
print(f"Headless: {config.headless}")

# With explicit overrides
config = OSWConfig(
    base_url="https://my-osw-instance.example.com",
    browser="firefox",
    headless=True,
)
```

## Login and Verify

Log in to an OSL instance and verify the main page loads.

```python
from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.login import LoginPage

config = OSWConfig.from_env()
driver = create_driver(config)

try:
    login_page = LoginPage(driver, config)
    login_page.login()

    driver.get(config.base_url.rstrip("/") + "/wiki/Main_Page")
    if "Main Page" in driver.page_source:
        print("Login successful — Main Page loaded.")
finally:
    driver.quit()
```

## Schema Path Utilities

Convert between JSON schema dot paths and HTML form bracket names.

```python
from osw_selenium.utils import (
    name_to_schema_path,
    schema_path_to_name,
    schema_path_to_property_checkbox_id,
)

# Dot notation -> bracket notation
name = schema_path_to_name("root.label.0.text")
# Result: root[label][0][text]

# Bracket notation -> dot notation
path = name_to_schema_path("root[label][0][text]")
# Result: root.label.0.text

# Property checkbox ID
checkbox_id = schema_path_to_property_checkbox_id("root.orderer")
# Result: root-orderer
```

## Create ELN Entry

Create an ELN entry with inline organization and person references.

```python
from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.login import LoginPage
from osw_selenium.pages.json_editor import JsonEditorPage

config = OSWConfig.from_env()
driver = create_driver(config)

try:
    # Login
    LoginPage(driver, config).login()

    # Open the create-instance form
    editor = JsonEditorPage(driver, config)
    editor.open_create_instance_form(
        category="Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"
    )

    # Fill fields
    editor.fill_editor_field(schemapath="root.label.0.text", value="My ELN entry")
    editor.save_editor()
finally:
    driver.quit()
```
