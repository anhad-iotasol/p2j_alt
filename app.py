import streamlit as st
import json
from pathlib import Path
from controller.history_controller import clear_history_all,load_history
from views.form_creation_view import form_creation_view
from views.form_view import form_view
from paths import TABLE_LIST_PATH,HISTORY_PATH,ALT_HISTORY_PATH



#table_list = json.loads(Path(TABLE_LIST_PATH).read_text())
#table_names = [table['name'] for table in table_list]

#select_options = ["Form"]+table_names
#entity = st.selectbox("Select entity",select_options)
#print(entity)
entity="Form"
chat_history_alt = json.loads(Path(ALT_HISTORY_PATH).read_text())
chat_history = load_history(entity,HISTORY_PATH)

st.button("Clear History",key="clearbtn",on_click=clear_history_all,args=[entity,chat_history,chat_history_alt])
st.title(entity)
#if entity=="Form": form_creation_view(chat_history,chat_history_alt)
form_creation_view(chat_history,chat_history_alt)
#else : form_view(entity,chat_history)