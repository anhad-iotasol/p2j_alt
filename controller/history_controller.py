import streamlit as st
import json
from pathlib import Path
from paths import HISTORY_PATH

def update_history(message,entity,chat_history):
    st.session_state.messages.append(message)
    chat_history[entity].append(message)
    with open(HISTORY_PATH,'w') as file:
        json.dump(chat_history,file,indent=4)

def clear_history(entity,chat_history):
    st.session_state.messages = []
    chat_history[entity] = []
    with open(HISTORY_PATH,'w') as file:
        json.dump(chat_history,file,indent=4)


def load_history(entity):
    chat_history = json.loads(Path(HISTORY_PATH).read_text())
    if entity not in chat_history.keys() or not chat_history[entity]:
        st.session_state.messages = []
        chat_history[entity] = []
        with open(HISTORY_PATH,'w') as file:
            json.dump(chat_history,file,indent=4)
#    elif not "messages" in st.session_state:
#        st.session_state.messages = chat_history[entity]
    else:
        st.session_state.messages = chat_history[entity]
    return chat_history