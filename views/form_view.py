import streamlit as st
from services.llm_parser.models.PaLM2 import model
from services.llm_parser import form_template_conversational
import json
from pathlib import Path
import pandas as pd
from controller.history_controller import update_history
from controller.form_controller import form_controller
from paths import TABLE_LIST_PATH,TABLE_BASE_PATH


def form_view(entity:str,chat_history):

    table_name=entity
    #table_name = list(json_data['components']['schemas'].keys())[0]
    table_list = json.loads(Path(TABLE_LIST_PATH).read_text())
    table_json = [table for table in table_list if table['name']==table_name][0]
    template = form_template_conversational(table_json['schema']['properties'])


    # calls the flask app endpoint using the data.
    def onOk(table_name:str,action:str,data):
        def modify_table():
            #response = send_req(table_name,data,action)
            response = form_controller[action](table_name,data)
            print(response)
        return modify_table

    # checking for JSON validity for parsing.
    def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True


    df = pd.read_csv(f"{TABLE_BASE_PATH}{table_name}.csv")
    st.table(df)

    # displaying the user and AI chat history as previous chat messages.
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    if prompt := st.chat_input("enter prompt"):
        st.chat_message("user").markdown(prompt)

        update_history({
            "role": "user",
            "content" : prompt
        },entity,chat_history)
        

        # Using the prompt, and history to form the LLM template
        templated_prompt = template.format(history=str(st.session_state.messages),input=prompt)
        response = model(templated_prompt)

        with st.chat_message("assistant"):
            st.markdown(response)
            if is_json(response):
                response_data = json.loads(response)
                action = response_data["action"]
                data = response_data["form_data"]
                st.button("Ok",on_click=onOk(table_name,action,data),key="json2streamlitAddData")

        update_history({
            "role" : "assistant",
            "content": response
        },entity,chat_history)