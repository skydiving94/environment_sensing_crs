"""
This is a sql agent. He is specialized in 
Writing SQL and fetch data from the database
Each agent should have __main__ and can be used and tested independently 
"""
import argparse
import asyncio
import os
import sqlite3

import pandas as pd
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# LangChain automatically loads OPENAI_API_KEY from the environment.
# Omitting it avoids the Pydantic v1 vs v2 SecretStr type conflict.
llm = ChatOpenAI(
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


async def main():
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

    # Utilize asynchronous invocation for LangChain
    resp = await llm.ainvoke(message, temperature=0.0, max_tokens=120, top_p=1.0, timeout=10)
    print('LLM response:\n', resp.content)

    print('Querying the database with LLM-generated query text.')

    # Cast content to a strict string to satisfy pandas,
    # and use type: ignore to bypass the Pylance chunksize/asyncio bug
    sql_query = str(resp.content)
    # type: ignore
    df = await asyncio.to_thread(pd.read_sql_query, sql=sql_query, con=conn)
    print(df)


if __name__ == '__main__':
    asyncio.run(main())
