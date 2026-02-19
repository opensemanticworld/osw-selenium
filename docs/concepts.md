# Concepts

This page explains the core ideas behind osw-selenium for users who
want to understand *why* the library is designed the way it is.

## The Page Object Pattern

osw-selenium uses the **Page Object Model** (POM), a design pattern from
the Selenium community where each distinct page or component in the UI
gets its own class.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Without Page Objects
:class-header: sd-bg-danger sd-text-white sd-font-weight-bold

```python
# Fragile -- raw Selenium everywhere
driver.find_element(By.ID, "wpName1").send_keys("Admin")
driver.find_element(By.ID, "wpPassword1").send_keys("pass")
driver.find_element(By.ID, "wpLoginAttempt").click()
```
:::

:::{grid-item-card} With Page Objects
:class-header: sd-bg-success sd-text-white sd-font-weight-bold

```python
# Clean -- intent is clear, details encapsulated
login_page = LoginPage(driver, config)
login_page.login()
```
:::

::::

**Benefits:**

- **Readability** -- Test code reads like a user story.
- **Maintainability** -- Selector changes are isolated to one class.
- **Reuse** -- The same page object works in scripts and pytest tests.

## Editor Level Tracking

OpenSemanticLab's JSON editor supports *nested inline editors*. When you
click "Create inline" on a reference field, a new editor opens inside the
current one. osw-selenium tracks this nesting automatically.

```python
editor.open_create_instance_form(category="Category:...")  # level 0
editor.create_inline(schemapath="root.orderer")            # level 0 -> 1
editor.fill_editor_field(schemapath="root.label.0.text", value="Org Name")
editor.save_editor()                                       # level 1 -> 0
editor.save_editor()                                       # level 0 -> -1
```

:::{admonition} Key insight
:class: important

You never need to manually track which editor is active.
`fill_editor_field()` automatically targets the innermost open editor
by using the `_editor_id` that corresponds to the current `_editor_level`.
:::

See the {doc}`architecture` page for a full state machine diagram.

## Schema Paths

In OSL's JSON editor, every form field maps to a path in the underlying
JSON Schema. osw-selenium lets you address fields using **dot notation**:

```text
root.label.0.text     ->  The text of the first label
root.orderer          ->  The orderer reference field
root.actionees.0      ->  The first actionee in the array
```

Internally, these are converted to HTML form `name` attributes using
bracket notation (`root[label][0][text]`) and then composed into CSS
selectors for Selenium to locate the element.

:::{admonition} Roundtrip guarantee
:class: note

`name_to_schema_path(schema_path_to_name(path))` always returns the
original path. Both functions are tested with doctests.
:::

## Fixture Design

The pytest fixtures in `conftest.py` follow a layered design:

Session-scoped (created once per test run)
: `osw_config` -- reads env vars
: `driver` -- starts the browser
: `logged_in_driver` -- logs in via `LoginPage`

Function-scoped (created per test)
: `login_page` -- fresh `LoginPage` wrapping the shared driver
: `json_editor` -- fresh `JsonEditorPage` wrapping the logged-in driver

:::{admonition} Extending with your own fixtures
:class: tip

Copy `conftest.py` into your test directory and add new page objects as
needed. The pattern is always the same: create a function-scoped fixture
that takes `logged_in_driver` and `osw_config` and returns a new page object.
:::
