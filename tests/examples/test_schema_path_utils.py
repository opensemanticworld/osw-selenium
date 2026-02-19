"""Tests for examples/schema_path_utils.py — verify conversion functions work."""

from __future__ import annotations

from osw_selenium.utils import (
    name_to_schema_path,
    schema_path_to_name,
    schema_path_to_property_checkbox_id,
)


def test_schema_to_name_nested():
    """Dot-separated path converts to bracket notation."""
    assert schema_path_to_name("root.label.0.text") == "root[label][0][text]"


def test_name_to_schema_nested():
    """Bracket notation converts to dot-separated path."""
    assert name_to_schema_path("root[label][0][text]") == "root.label.0.text"


def test_roundtrip_dot_to_bracket_to_dot():
    """Converting schema -> name -> schema produces the original."""
    original = "root.label.0.text"
    assert name_to_schema_path(schema_path_to_name(original)) == original


def test_roundtrip_bracket_to_dot_to_bracket():
    """Converting name -> schema -> name produces the original."""
    original = "root[label][0][text]"
    assert schema_path_to_name(name_to_schema_path(original)) == original


def test_simple_root_unchanged():
    """A bare 'root' with no nesting passes through unchanged."""
    assert schema_path_to_name("root") == "root"
    assert name_to_schema_path("root") == "root"


def test_property_checkbox_id():
    """Last dot is replaced with a dash for property checkbox IDs."""
    assert schema_path_to_property_checkbox_id("root.orderer") == "root-orderer"
    assert schema_path_to_property_checkbox_id("root.actionees") == "root-actionees"
