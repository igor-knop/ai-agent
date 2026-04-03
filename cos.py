from openai import OpenAI
from langchain.tools import tool
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

client = OpenAI(api_key = api_key)

    