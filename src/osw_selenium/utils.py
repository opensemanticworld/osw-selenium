"""Utility functions for schema path conversions and parameter normalization."""

from __future__ import annotations

import re


def name_to_schema_path(name: str) -> str:
    """Convert a form field name to a dot-separated schema path.

    Args:
        name: Form field name like ``root[label][0][text]``.

    Returns:
        Dot-separated path like ``root.label.0.text``.

    Example:
        >>> name_to_schema_path("root[label][0][text]")
        'root.label.0.text'
        >>> name_to_schema_path("root")
        'root'
    """
    name = name.replace("][", ".")
    name = name.replace("[", ".")
    name = name.replace("]", "")
    return name


def schema_path_to_name(schemapath: str) -> str:
    """Convert a dot-separated schema path to a form field name.

    Args:
        schemapath: Dot-separated path like ``root.label.0.text``.

    Returns:
        Form field name like ``root[label][0][text]``.

    Example:
        >>> schema_path_to_name("root.label.0.text")
        'root[label][0][text]'
        >>> schema_path_to_name("root")
        'root'
    """
    # Replace first '.' with '[', matching the JS: schemapath.replace('.','[')
    schemapath = schemapath.replace(".", "[", 1)
    # Replace remaining '.' with ']['
    schemapath = schemapath.replace(".", "][")
    # Close the bracket if we opened one
    if "[" in schemapath:
        schemapath += "]"
    return schemapath


def schema_path_to_property_checkbox_id(schemapath: str) -> str:
    """Convert a schema path to the corresponding property checkbox ID.

    Replaces the last ``.`` in the schema path with ``-``.

    Args:
        schemapath: Dot-separated path like ``root.orderer``.

    Returns:
        Checkbox ID like ``root-orderer``.

    Example:
        >>> schema_path_to_property_checkbox_id("root.orderer")
        'root-orderer'
        >>> schema_path_to_property_checkbox_id("root.actionees")
        'root-actionees'
    """
    return re.sub(r"\.(?=[^.]*$)", "-", schemapath)
