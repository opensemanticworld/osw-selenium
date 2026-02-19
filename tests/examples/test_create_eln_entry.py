"""Tests for examples/create_eln_entry.py — verify ELN entry creation against a live OSL instance."""

from __future__ import annotations

import pytest

from osw_selenium.pages.json_editor import JsonEditorPage

pytestmark = pytest.mark.integration

ELN_ENTRY_CATEGORY = "Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"


def test_json_editor_page_has_expected_locators():
    """JsonEditorPage exposes the expected locator constants (offline check)."""
    assert JsonEditorPage.CREATE_INSTANCE_TAB[1] == "ca-create-instance"
    assert JsonEditorPage.EDIT_DATA_TAB[1] == "ca-edit-data"


def test_create_eln_entry_with_inline_records(json_editor):
    """Full ELN entry creation workflow: inline org + inline person."""
    editor = json_editor

    editor.open_create_instance_form(category=ELN_ENTRY_CATEGORY)
    editor.fill_editor_field(schemapath="root.label.0.text", value="Test label")

    # Inline organization
    editor.add_additional_property(schemapath="root.orderer")
    editor.fill_editor_field(schemapath="root.orderer", value="")
    editor.create_inline(schemapath="root.orderer")
    editor.fill_editor_field(schemapath="root.label.0.text", value="Test Org")
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.orderer", expected="Test Org")

    # Inline person in actionees array
    editor.add_additional_property(schemapath="root.actionees")
    editor.add_array_element(schemapath="root.actionees")
    editor.fill_editor_field(schemapath="root.actionees.0", value="")
    editor.create_inline(schemapath="root.actionees.0")
    editor.fill_editor_field(schemapath="root.first_name", value="Jane")
    editor.fill_editor_field(schemapath="root.surname", value="Doe")
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.actionees.0", expected="Jane Doe")

    # Save main form
    editor.save_editor()
    editor.wait(3)
