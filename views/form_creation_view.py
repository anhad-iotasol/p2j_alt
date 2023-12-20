import streamlit as st
from services.llm_parser import generate_form_converse
import json
from pathlib import Path
import pandas as pd
from services.form_service import build_df
from services.llm_parser.generate_schema import generate_table
from controller.history_controller import update_history
from paths import TABLE_LIST_PATH
from services.Frappe import schema_to_json
from services.Frappe.REST_service import submit_form
import streamlit.components.v1 as components
from services.Frappe.REST_service import frappe_login
from dotenv import load_dotenv,find_dotenv
import os

_ = load_dotenv(find_dotenv())

def form_creation_view(chat_history,entity="Form"):

    def preview_form(response: dict):
         #def publish_json():
        response_table = generate_table(response)
        table_list: list = []
        table_list.append(response_table)
        with open(TABLE_LIST_PATH, 'w') as file:
            json.dump(table_list, file, indent=4)
        request_body = schema_to_json(response_table)
        submit_form(request_body)
        return

    def response_to_df(response):
        display_json = {"Property": ["Data Type","Default"]}
        properties = response['properties']
        for field in properties:
            display_json.update({field['name']:[field['type'],field['default']]})
        df = pd.DataFrame(display_json)
        return df

    def parse_response(response:str):
        response_dict = json.loads(response)
        table_name = response_dict['name']
        required = response_dict['required']
        df = response_to_df(response_dict)
        return [table_name,required,df]

    # displaying the user and AI chat history as previous chat messages.
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            #st.markdown(message['content'])
            if message['role'] == 'user' : st.markdown(message["content"])
            elif message['role'] == 'assistant' : 
                table_name,required,df = parse_response(message['content'])
                st.markdown(table_name)
                st.markdown(f"Required: {required}")
                st.dataframe(df)

    if prompt := st.chat_input("enter prompt"):
        st.chat_message("user").markdown(prompt)

        #update the history with the user input
        update_history({
            "role": "user",
            "content" : prompt
        },entity,chat_history)

        response_json = generate_form_converse(prompt,history=str(st.session_state.messages))

        with st.chat_message("assistant"):
            response_dict = json.loads(response_json)
            preview_form(response_dict)
            table_name = response_dict['name']
            #sid = frappe_login()
            #components.iframe(f"http://testsite.test:8000/app/doctype/{table_name}?sid={sid}&parent=DocType",height=600,scrolling=True)
            #components.iframe(f"{os.environ['PDF_LINK']}&sid={sid}",height=600,scrolling=True)
            #required = response_dict['required']
            #df = response_to_df(response_dict)
            #st.markdown(table_name)
            #st.markdown(f"Required: {required}")
            #st.dataframe(df)
            #publish_json = st.button("Publish", on_click=onPublish,args=[response_dict],key="form_publish")
        update_history({
            "role" : "assistant",
            "content" : response_json
        },entity,chat_history)
        


