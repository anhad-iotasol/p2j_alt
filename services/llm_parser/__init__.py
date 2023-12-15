from services.llm_parser.models.PaLM2 import model
from services.llm_parser.response_schema import Form
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
import json

# Different experimental templates to use in different situations.

def form_template_conversational(form_schema):
    template = """
    You are an AI assistant helping users in performing an action on entries of a form, the schema of which has been provided to you. The conversation takes place 
    in multiple stages. use the conversation history in order to determine which stage you are in, and give out the appropriate response.

    The action will be one of the following: Create, Read, Update, Delete

    stage 1: use the schema to extract extract the form properties in the form of key-value pairs and output the data as a json string. Also determine the action the user is performing on the form,
            which is one of the four possibilities mentioned before. The schema provided is a json object, with each key being the name of the property, and the value is an object containing the data type and default value.

            your output should look like this: 

            {{
                action: "action determined goes here",
                form_data: {{
                    "property name 1" : "property value 1",
                    "property name 2" : "property value 2"
                }}
            }}
            
            and so on for all properties listed. Some properties may not be provided.

            Follow up the JSON with a message, in which you list the properties in the schema which have not been provided in the previous message.
            And ask if the would like to add any of them, or change any existing properties. Your output should look like this - 

            (json output)

            Would you like to add any of the following properties or change any of the values shown above?
            1. missing property 1
            2. missing property 2

            and so on. If all properties are provided, omit the follow up message.

            schema: {form_schema}

    stage 2: If the user responds with negative or is satisfied with the current response, move to step 3.
            If the user replies with information on additional properties, add those properties to the previous JSON and give the same output as step 1 but with the
            updated JSON, and then repeat step 2 again until the user replies in negative or is satisfied, in which case go to step 3.

    stage 3: Display the only final JSON as your output without any additional text.

    Current conversation: 
    {history}

    Human: {input}
    assistant: 
    """
    prompt_template = PromptTemplate(input_variables=["history","input","form_schema"], template= template)
    partial_prompt = prompt_template.partial(form_schema=str(form_schema))
    return partial_prompt

def generate_form_converse(text: str,history):
    review_template = """\
    You are an AI assistant and an expert output parser.

    You will be involved in a conversation with the user. In the first step when no prior prompt is given, you are to extract key information from the prompt
    regarding the form and output it according to the schema below.

    Also note that the prompt does not give the information on a form explicitly. The situation will be that of a user requesting entry of
    data assuming that the form has been created. Do not use the data but, use the prompt to determine what fields will be present and 
    what their data types should be. Also guess what fields should be required on your own.

    Do not include any special characters like "-" in the field names

    {{
        "name" : (contains name of the form),
        "required" : (list of required properties, leave as empty list if not mentioned)
        "properties" : (list of properties, each property containing details of property name, type, and default value in key value pairs)
    }}
    
    examples = [
    {{
        "prompt" : "Add a new supplier by the name of PRS & Co., they are located in 221B Baker Street, California, United States. They come under the ERP Type SAP, with
        ERP ID of AA10110, DUNS is 694761. This is low risk, a non-profit supplier, with a performance rating of 5.0 out of 10.",
        "answer" : {{
            "name" : "Suppliers",
            "required" : ["Name","ERP ID","DUNS"],
            "properties" : [
                {{
                    "name": "Name",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "Address",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "State",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "Country",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "ERP Type",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "ERP ID",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "DUNS",
                    "type" : "integer",
                    "default" : ""
                }},
                {{
                    "name" : "risk level",
                    "type" : "string",
                    "default" : ""
                }},
                {{
                    "name" : "non profit",
                    "type" : "boolean",
                    "default" : "False"
                }},
                {{
                    "name" : "performance rating",
                    "type" : "float",
                    "default" : ""
                }}
            ]
        }}
    }}
    ]

    {format_instructions}

    You are provided the conversation history in addition to other instructions. If the history is blank, the first prompt will be to generate the json as per the instructions 
    given above. If there has been a prompt entered in the history already, the subsequent prompts will request to make changes in the output given before. 
    Use the conversation history in order to determine the appropriate response.

    history: {history}

    human: {query}

    assistant: 

    """

    parser = PydanticOutputParser(pydantic_object=Form)

    prompt = PromptTemplate(template=review_template, input_variables=[
                            "query"], partial_variables={'format_instructions': parser.get_format_instructions(), 'history': history})

    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=review_template)

    messages = prompt.format_messages(
        query=text, format_instructions=format_instructions,history=history)
    response = model(messages[0].content)
    parsed_response = parser.parse(response).json()
    #dict_data = json.loads(parsed_response)
    #print(str(dict_data)[45:55])
    #table = generate_table(dict_data)
    return parsed_response