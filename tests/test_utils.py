"""Unit tests for schema path utility functions — no browser needed."""

from __future__ import annotations

from osw_selenium.utils import name_to_schema_path, schema_path_to_name, schema_path_to_property_checkbox_id


def test_name_to_schema_path_nested():
    assert name_to_schema_path("root[label][0][text]") == "root.label.0.text"


def test_name_to_schema_path_simple():
    assert name_to_schema_path("root") == "root"


def test_name_to_schema_path_single_level():
    assert name_to_schema_path("root[label]") == "root.label"


def test_schema_path_to_name_nested():
    assert schema_path_to_name("root.label.0.text") == "root[label][0][text]"


def test_schema_path_to_name_simple():
    assert schema_path_to_name("root") == "root"


def test_schema_path_to_name_single_level():
    assert schema_path_to_name("root.label") == "root[label]"


def test_roundtrip():
    original = "root.label.0.text"
    assert name_to_schema_path(schema_path_to_name(original)) == original


def test_roundtrip_reverse():
    original = "root[label][0][text]"
    assert schema_path_to_name(name_to_schema_path(original)) == original


def test_property_checkbox_id():
    assert schema_path_to_property_checkbox_id("root.orderer") == "root-orderer"


def test_property_checkbox_id_nested():
    assert schema_path_to_property_checkbox_id("root.actionees") == "root-actionees"
