# Query SQL Database action
from typing import List, Dict
import os
import sqlite3
import pandas as pd

# TODO: Init this database connection in a better way
conn = sqlite3.connect('/Users/zpeng/project/environment_sensing_crs/dataset/movielens.db')

def do_query_sql_database(sql_query: str) -> str:
    """
    Given a list of results, use LLM to generate a response.
    :param results: A list of results collected.
    :return: A string as the response.
    """
    res = pd.read_sql_query(sql_query, conn)

    return res


if __name__ == "__main__":
    print(do_query_sql_database("SELECT * FROM movies LIMIT 5"))
    print(do_query_sql_database("SELECT * FROM ratings LIMIT 5"))
    print(do_query_sql_database("SELECT * FROM tags LIMIT 5"))