import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

open_ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
