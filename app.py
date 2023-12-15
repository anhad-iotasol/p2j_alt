import streamlit as st
import json
from pathlib import Path
from controller.history_controller import clear_history,load_history
from views.form_creation_view import form_creation_view
from views.form_view import form_view
from paths import TABLE_LIST_PATH



table_list = json.loads(Path(TABLE_LIST_PATH).read_text())
table_names = [table['name'] for table in table_list]

select_options = ["Form"]+table_names
entity = st.selectbox("Select entity",select_options)
#print(entity)
chat_history = load_history(entity)

st.button("Clear History",key="clearbtn",on_click=clear_history,args=[entity,chat_history])
st.title(entity)
if entity=="Form": form_creation_view(chat_history)
else : form_view(entity,chat_history)