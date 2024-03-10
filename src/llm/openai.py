import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


openai_llm = ChatOpenAI(  # type: ignore
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model=os.getenv('OPENAI_TEXT_MODEL'))  # type: ignore
