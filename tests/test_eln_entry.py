"""Integration test for ELN entry creation — requires a running OSW instance.

Ported from migration/tests/start_test.js 'Create ELN entry' scenario.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration

ELN_ENTRY_CATEGORY = "Category:OSW0e7fab2262fb4427ad0fa454bc868a0d"


def test_create_eln_entry(json_editor):
    """Create an ELN entry with inline organization and person."""
    editor = json_editor

    # 1. Open create instance form for ELN Entry
    editor.open_create_instance_form(category=ELN_ENTRY_CATEGORY)

    # 2. Fill label
    editor.fill_editor_field(schemapath="root.label.0.text", value="Test label")

    # 3. Add orderer property
    editor.add_additional_property(schemapath="root.orderer")
    editor.fill_editor_field(schemapath="root.orderer", value="")

    # 4. Create inline org — cancel first, then create and save
    editor.create_inline(schemapath="root.orderer")
    editor.cancel_editor()
    editor.create_inline(schemapath="root.orderer")
    org_name = "Test Org label 0"
    editor.fill_editor_field(schemapath="root.label.0.text", value=org_name)
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.orderer", expected=org_name)

    # 5. Add actionees array
    editor.add_additional_property(schemapath="root.actionees")
    editor.add_array_element(schemapath="root.actionees")
    editor.fill_editor_field(schemapath="root.actionees.0", value="")

    # 6. Create inline person
    editor.create_inline(schemapath="root.actionees.0")
    act_name = "Person 0"
    editor.fill_editor_field(schemapath="root.first_name", value="Test")
    editor.fill_editor_field(schemapath="root.surname", value=act_name)
    editor.save_editor()
    editor.assert_field_has_value(schemapath="root.actionees.0", expected="Test " + act_name)

    # 7. Save main form
    editor.save_editor()
    editor.wait(3)
