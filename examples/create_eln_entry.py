"""Example: Create an ELN entry with inline organization and person records.

Requires MW_SITE_SERVER and MW_ADMIN_PASS environment variables.
Demonstrates the full JSON editor workflow:
  - Opening a create-instance form
  - Filling fields by schema path
  - Adding additional properties
  - Creating and saving inline (nested) editors
  - Asserting field values
"""

from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.json_editor import JsonEditorPage
from osw_selenium.pages.login import LoginPage

ELN_ENTRY_CATEGORY = "Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"

config = OSWConfig.from_env()
driver = create_driver(config)

try:
    # Log in first
    login_page = LoginPage(driver, config)
    login_page.login()

    # Open the ELN entry creation form
    editor = JsonEditorPage(driver, config)
    editor.open_create_instance_form(category=ELN_ENTRY_CATEGORY)

    # Fill the label
    editor.fill_editor_field(schemapath="root.label.0.text", value="Test label")

    # Add and fill orderer via inline organization
    editor.add_additional_property(schemapath="root.orderer")
    editor.fill_editor_field(schemapath="root.orderer", value="")
    editor.create_inline(schemapath="root.orderer")
    editor.fill_editor_field(schemapath="root.label.0.text", value="Test Org")
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.orderer", expected="Test Org")

    # Add actionees array with an inline person
    editor.add_additional_property(schemapath="root.actionees")
    editor.add_array_element(schemapath="root.actionees")
    editor.fill_editor_field(schemapath="root.actionees.0", value="")
    editor.create_inline(schemapath="root.actionees.0")
    editor.fill_editor_field(schemapath="root.first_name", value="Jane")
    editor.fill_editor_field(schemapath="root.surname", value="Doe")
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.actionees.0", expected="Jane Doe")

    # Save the main form
    editor.save_editor()
    print("ELN entry created successfully.")
finally:
    driver.quit()
