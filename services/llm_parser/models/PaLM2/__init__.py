from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
import google.generativeai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

model = GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'])
