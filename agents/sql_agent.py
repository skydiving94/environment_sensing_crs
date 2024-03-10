"""
This is a sql agent. He is specialized in 
Writing SQL and fetch data from the database
Each agent should have __main__ and can be used and tested independently 
"""
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv() # .env is not in the the same directory, why is it working? 
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("You must set your OPENAI_API_KEY in Environment Variables")

# print(os.getenv("OPENAI_API_KEY"))


"""
This script sets up the sqlite database for the movie dataset. 
It creates a database locally.
"""
import sqlite3
import pandas as pd



# Test langchain-openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")

system_template = """
You are an expert in SQL programming. You are asked to write a SQL query according to user request.
Format your response as a SQL query on sqlite database. Output only SQL query.

List of available tables:
    - movies: movieId, title, genres
    
"What is genres is the movie 'Toy Story (1995)'?"
"""
human_template = "What is genres is the movie 'Toy Story (1995)'?"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

resp = llm.invoke(system_template, temperature=0.0, max_tokens=120, top_p=1.0, timeout=10)
print("LLM response: ", resp.content)

conn = sqlite3.connect('/Users/zhejianpeng/project/environment_sensing_crs/dataset/movielens.db')

print("Use LLM response directly to query database", pd.read_sql_query(resp.content, conn))

# # Check each table's row count
# conn = sqlite3.connect('/Users/zhejianpeng/project/environment_sensing_crs/dataset/movielens.db')
# tables = ['genome_scores', 'genome_tags', 'links', 'movies', 'ratings', 'tags']
# for table in tables:
#     print("Table: {}, row count: {}".format(table, pd.read_sql_query("SELECT COUNT(*) FROM {}".format(table), conn)))

