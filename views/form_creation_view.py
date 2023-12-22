import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv,find_dotenv
from paths import TABLE_LIST_PATH,HISTORY_PATH,ALT_HISTORY_PATH
from services.llm_parser import generate_form_converse, chatbot_message
from services.llm_parser.generate_schema import generate_table
from services.Frappe import schema_to_json
from services.Frappe.REST_service import submit_form
from services.Frappe.REST_service import frappe_login,onPublish
from controller.history_controller import update_history


_ = load_dotenv(find_dotenv())

def form_creation_view(chat_history,chat_history_alt,entity="Form"):
    

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
    #for message in st.session_state["messages"]:
    for message in chat_history_alt[entity]:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])
            #if message['role'] == 'user' : st.markdown(message["content"])
            #elif message['role'] == 'assistant' : 
            #    table_name,required,df = parse_response(message['content'])
            #    st.markdown(table_name)
            #    st.markdown(f"Required: {required}")
            #    st.dataframe(df)
    #st.session_state.initial_prompt = ""

    if prompt := st.chat_input("enter prompt"):
        st.chat_message("user").markdown(prompt)
        #if not 'initial_prompt' in st.session_state.keys(): st.session_state.initial_prompt = prompt
        #update the history with the user input
        update_history({
            "role": "user",
            "content" : prompt
        },entity,chat_history,HISTORY_PATH)
        update_history({
            "role": "user",
            "content" : prompt
        },entity,chat_history_alt,ALT_HISTORY_PATH)
        #print(st.session_state.initial_prompt)
        response_json = generate_form_converse(prompt,history=str(st.session_state.messages))
        chatbot_response = chatbot_message(prompt,history=str(st.session_state.messages))

        with st.chat_message("assistant"):
            response_dict = json.loads(response_json)
            preview_form(response_dict)
            table_name = response_dict['name']
            st.markdown(chatbot_response)
          #  st.markdown()
            if chat_history[entity]: initial_prompt = chat_history[entity][0]['content']
            publish_json = st.button("Publish", on_click=onPublish,args=[initial_prompt,table_name],key="form_publish")
        update_history({
            "role" : "assistant",
            "content" : response_json
        },entity,chat_history,HISTORY_PATH)
        update_history({
            "role" : "assistant",
            "content" : chatbot_response
        },entity,chat_history_alt,ALT_HISTORY_PATH)
        


