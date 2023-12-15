import json
from pathlib import Path
from services.Frappe.type_mapping import type_mapping
TABLE_LIST_PATH = './model/table_list.json'

default_permissions= [
        {
            "role" : "System Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 0,
            "cancel": 0,
            "delete": 1,
            "amend": 0,
            "report": 1,
            "export": 1,
            "import": 0,
            "share": 1,
            "print": 1,
            "email": 1
        }
]


def schema_to_json(form_schema):
    form_json = dict({
        "module" : "Custom",
        "fields" : [],
        "permissions" : default_permissions
    })
    form_json['name'] = form_schema['name']
    properties  = form_schema['schema']['properties']
    for field in properties:
        field_data = dict({
            "label" : field,
            "fieldtype" : type_mapping[properties[field]['type']],
        })
        if properties[field]['default']: field_data['default'] = properties[field]['default']
        form_json['fields'].append(field_data)
    return form_json

table_schema = json.loads(Path(TABLE_LIST_PATH).read_text())[0]

frappe_body = schema_to_json(table_schema)
with open('./json_output.json','w') as file:
    json.dump(frappe_body,file,indent=4)

