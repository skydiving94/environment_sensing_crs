"""
This is a sql agent. He is specialized in 
Writing SQL and fetch data from the database
Each agent should have __main__ and can be used and tested independently 
"""
import argparse
import os
import sqlite3

import pandas as pd
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(  # type: ignore
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model=os.getenv('OPENAI_TEXT_MODEL', default='')
)

system_template = '''
You are an expert in SQL programming. You are asked to write a SQL query according to user request.
Format your response as a SQL query on sqlite database. 
Output only the SQL query, no extra characters.

List of available tables:
    - movies: movieId, title, genres
    - genome_scores: movieId, tagId, relevance
    - genome_tags: tagId, tag
    - links: movieId, imdbId, tmdbId
    - ratings: userId, movieId, rating, timestamp
    - tags: userId, movieId, tag, timestamp
'''
# human_template = 'What genres is the movie 'Toy Story (1995)'?'
human_template = 'What is the highest rating movie in Comedy genres?'


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('db_path', type=str)

    args = arg_parser.parse_args()

    db_path = args.db_path
    conn = sqlite3.connect(db_path)

    chat_prompt = ChatPromptTemplate.from_messages([
        ('system', system_template),
        ('human', human_template),
    ])

    message = chat_prompt.format_messages()

    resp = llm.invoke(message, temperature=0.0, max_tokens=120, top_p=1.0, timeout=10)
    print('LLM response:\n', resp.content)
    print('Querying the database with LLM-generated query text.')
    print(pd.read_sql_query(resp.content, conn))
    pass


if __name__ == '__main__':
    main()
