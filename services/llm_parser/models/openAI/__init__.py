from langchain.llms.openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

model = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'],model='gpt-3.5-turbo')