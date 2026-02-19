"""Example: Convert between JSON schema paths and HTML form field names.

OSL's JSON editor uses dot-separated schema paths internally
(e.g. ``root.label.0.text``) but renders HTML inputs with bracket-style
names (e.g. ``root[label][0][text]``). These utilities convert between the two.
"""

from osw_selenium.utils import (
    name_to_schema_path,
    schema_path_to_name,
    schema_path_to_property_checkbox_id,
)

# Schema path (dot notation) -> form field name (bracket notation)
schema = "root.label.0.text"
name = schema_path_to_name(schema)
print(f"Schema path: {schema}")
print(f"Field name:  {name}")
# Output: root[label][0][text]

# Form field name -> schema path (reverse)
restored = name_to_schema_path(name)
print(f"\nRestored:    {restored}")
print(f"Roundtrip OK: {restored == schema}")

# Property checkbox IDs replace the last '.' with '-'
prop_path = "root.orderer"
checkbox_id = schema_path_to_property_checkbox_id(prop_path)
print(f"\nProperty path:   {prop_path}")
print(f"Checkbox ID:     {checkbox_id}")
# Output: root-orderer
