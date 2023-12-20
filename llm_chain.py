from services.llm_parser.models.PaLM2 import model
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from services.llm_parser.response_schema import Form
import json
from pathlib import Path
from services.llm_parser import form_template_single
from paths import TABLE_LIST_PATH


def chatbot_message(text:str,history):
    review_template = """
        Given below is a history of messages made by a user and an AI assistant trying to create a form. 
        
        The prompts are given as if the user is trying to enter new data in an existing form, but this information is being used to create the form metadata instead.
        The values are irrelevant and should not be mentioned. 

        You are a different chatbot assistant. Your is informing the user that the changes they requested after the latest prompt have been reflected on the platform.
        Write an appropriate message detailing the changes made and give a response based on the latest prompt.

        If the history is empty, then the latest prompt will request form creation, so respond accordingly. If it is non-empty,
        then changes are being made to an existing form, so respond w.r.t to the changes made.

        For example - if a user is giving you details of a supplier form. Mention that the supplier form has been created and can be viewed on the platform,
        and also ask whether they would like to publish the form or make any further changes

        history : {history}

        human : {prompt}

        assistant: 
    """

    prompt = ChatPromptTemplate.from_template(template=review_template)
    messages = prompt.format_messages(
        prompt=text,history=history)
    response = model(messages[0].content)

    return response

history = json.loads(Path('./storage/chat_history.json').read_text())['Form']

text = "A new supplier - ABD International that is based in New Jersey, United States. This supplier is in the SAP with the ERP ID: C001452, DUNS - 292812311. The supplier is not a non-profit and its risk level is medium with a performance rating of 8.9 out of 10."
#text = "remove the performance rating field from the list of fields."
#chat_response = chatbot_message(text,history)
table_json = json.loads(Path(TABLE_LIST_PATH).read_text())[0]
#table_json = [table for table in table_list if table['name']==table_name][0]
template = form_template_single(table_json['schema']['properties'])
templated_prompt = template.format(input=text)
response = model(templated_prompt)
print(response)
#print(chat_response)