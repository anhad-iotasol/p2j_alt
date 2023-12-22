import os
from dotenv import load_dotenv, find_dotenv
from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings

_ = load_dotenv(find_dotenv())

model = GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'])
