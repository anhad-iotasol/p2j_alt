from services.llm_parser.models.PaLM2 import model
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from services.llm_parser.response_schema import Form

def generate_form_converse(text: str):
    review_template = """\
    You are an AI assistant and an expert output parser.

    Given the prompt, you are to extract key information from the prompt regarding the form and output it according to the schema below.
    Also note that the prompt does not give the information on a form explicitly. The situation will be that of a user requesting entry of
    data assuming that the form has been created. Do not use the data but, use the prompt to determine what fields will be present and 
    what their data types should be. Also guess what fields should be required on your own.

    {{
        "name" : (contains name of the form),
        "required" : (list of required properties, leave as empty list if not mentioned)
        "properties" : (list of properties, each property containing details of property name, type, and default value in key value pairs)
    }}
    
    examples = [
    {{
        "prompt" : "Please add a new entry for an employee joining us. Assign them the employee number 1234, name Lavish Aggarwal. Current address is A-74, Orange. ",
        "answer" : {{
            "name" : "Employees",
            "required" : ["employee number","employee name"],
            "properties" : [
                {{
                    "name": "employee number",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "employee name",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "address",
                    "type" : "string",
                    "default" : ""
                }}
            ]
        }}
    }},
    {{
        "prompt" : "A new guest, Anhad Bhati has joined us as well. Contact number is 9004933705, entered at 5:00PM, and will be leaving at 10:00PM",
        "answer" : {{
            "name" : "Guests",
            "required" : ["Name","contact number"],
            "properties" : [
                {{
                    "name" : "Name",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "contact number",
                    "type" : "integer",
                    "default" : ""
                }},
                {{
                    "name" : "Entry time",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "Exit time",
                    "type" : "string",
                    "default" : ""
                }}
            ]
        }}
    }}
    ]

    {format_instructions}

    human: {query}

    assistant: 

    """

    parser = PydanticOutputParser(pydantic_object=Form)

    prompt = PromptTemplate(template=review_template, input_variables=[
                            "query"], partial_variables={'format_instructions': parser.get_format_instructions()})

    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=review_template)

    messages = prompt.format_messages(
        query=text, format_instructions=format_instructions)
    response = model(messages[0].content)
    parsed_response = parser.parse(response).json()
    #dict_data = json.loads(parsed_response)
    #print(str(dict_data)[45:55])
    #table = generate_table(dict_data)
    return parsed_response

text = "A new supplier - ABD International that is based in New Jersey, United States. This supplier is in the SAP with the ERP ID: C001452, DUNS - 292812311. The supplier is not a non-profit and its risk level is medium with a performance rating of 8.9 out of 10."

response = generate_form_converse(text)

print(response)