# Architecture

This page explains the design of osw-selenium: the package structure,
class hierarchy, and the key patterns that hold it together.

## Package Structure

```text
src/osw_selenium/
├── __init__.py          # Public API re-exports
├── config.py            # OSWConfig dataclass
├── driver.py            # create_driver() factory
├── utils.py             # Schema path conversions
└── pages/
    ├── __init__.py      # Page object re-exports
    ├── base.py          # BasePage — shared browser helpers
    ├── login.py         # LoginPage — login flows
    └── json_editor.py   # JsonEditorPage — form CRUD + state machine
```

## Class Hierarchy

```{mermaid}
classDiagram
    class BasePage {
        +WebDriver driver
        +OSWConfig config
        +int timeout
        +navigate_to(path)
        +wait_for_element(locator, timeout)
        +wait_for_visible(locator, timeout)
        +wait_for_clickable(locator, timeout)
        +click(locator)
        +fill_field(locator, value)
        +scroll_and_click(locator)
        +scroll_and_fill(locator, value)
        +execute_js(script, *args)
    }

    class LoginPage {
        +login(username, password)
        +login_hidden(username, password)
    }

    class JsonEditorPage {
        -int _editor_level
        -str _editor_id
        +editor_level : int
        +editor_id : str
        +open_create_instance_form(category)
        +open_edit_instance_form(title)
        +fill_editor_field(schemapath, value)
        +create_inline(schemapath)
        +save_editor()
        +cancel_editor()
        +assert_field_has_value(schemapath, expected)
    }

    BasePage <|-- LoginPage
    BasePage <|-- JsonEditorPage
```

## Configuration Flow

```{mermaid}
flowchart LR
    ENV["Environment variables<br/>.env file"] --> from_env["OSWConfig.from_env()"]
    from_env --> config["OSWConfig<br/>(frozen dataclass)"]
    config --> create_driver["create_driver(config)"]
    create_driver --> Chrome["Chrome WebDriver"]
    create_driver --> Firefox["Firefox WebDriver"]
    config --> pages["Page Objects<br/>(BasePage, LoginPage, ...)"]
```

## Editor Level State Machine

`JsonEditorPage` manages a stack of nested editors. Each inline form
increments the level; saving or cancelling decrements it.

```{mermaid}
stateDiagram-v2
    [*] --> NoEditor : level = -1
    NoEditor --> Level0 : open_create/edit_instance_form()
    Level0 --> Level1 : create_inline()
    Level1 --> Level2 : create_inline()
    Level2 --> Level1 : save_editor() / cancel_editor()
    Level1 --> Level0 : save_editor() / cancel_editor()
    Level0 --> NoEditor : save_editor() / cancel_editor()
```

:::{admonition} How editor tracking works
:class: tip

Each time a nested editor opens, `_increment_editor_level()` queries
the DOM for all `.je-ready` elements and records the `id` of the one
at the current level index. When the editor saves or cancels,
`_decrement_editor_level()` does the reverse. This means
`fill_editor_field()` always targets the correct nested form.
:::

## Schema Path System

Fields are addressed using dot-separated paths that mirror the JSON schema
structure. The `utils.py` module converts between formats:

| Direction | Input | Output |
| --- | --- | --- |
| `schema_path_to_name` | `root.label.0.text` | `root[label][0][text]` |
| `name_to_schema_path` | `root[label][0][text]` | `root.label.0.text` |
| `schema_path_to_property_checkbox_id` | `root.orderer` | `root-orderer` |

```{mermaid}
flowchart LR
    user["User code<br/>schema path: root.label.0.text"] --> convert["schema_path_to_name()"]
    convert --> name["HTML name attr:<br/>root[label][0][text]"]
    name --> css["CSS selector:<br/>#editor_id [name='root[label][0][text]']"]
    css --> element["DOM Element"]
```

## Fixture Hierarchy

The `tests/conftest.py` provides a dependency chain of pytest fixtures:

```{mermaid}
flowchart TD
    osw_config["osw_config<br/>(session scope)"] --> driver["driver<br/>(session scope)"]
    osw_config --> logged_in["logged_in_driver<br/>(session scope)"]
    driver --> logged_in
    driver --> login_page["login_page<br/>(function scope)"]
    osw_config --> login_page
    logged_in --> json_editor["json_editor<br/>(function scope)"]
    osw_config --> json_editor
```

:::{admonition} Why session-scoped driver?
:class: note

Starting a browser is expensive. The `driver` fixture starts Chrome/Firefox
once and reuses it across all tests. The `logged_in_driver` logs in once;
session cookies persist automatically. Function-scoped page objects
(`login_page`, `json_editor`) are cheap to create since they just wrap
the shared driver.
:::
