
# Used to format the LLM response for form creation to a format desired by swagger.
def generate_table(llm_response: dict):
    table: dict = {
        "name": llm_response['name'],
        "schema": {
            "type": "object",
            "required": llm_response['required'],
            "properties": {}
        }
    }
    for field in llm_response['properties']:
        table["schema"]["properties"][field['name']] = {
            "type": field['type'],
            "default": field['default']
        }
    return table
