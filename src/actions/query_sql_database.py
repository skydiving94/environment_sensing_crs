import json
import os
import sqlite3
import string
from copy import deepcopy
from typing import Dict

import pandas as pd

from src.utils.general_utils import find_latest_information_with_substring
from src.actions import action_tool


@action_tool(name="do_query_sql_database")
def do_query_sql_database(**kwargs) -> Dict[str, str]:
    """
    Execute a SQL query against the connected database and return the results.
    """
    sql_query_key = find_latest_information_with_substring(
        list(kwargs.keys()), 'sql_query')
    if sql_query_key is None:
        return {}

    sql_query = kwargs[sql_query_key]
    print("Executing SQL Query: ", sql_query)
    sql_query_result = _do_query_sql_database(sql_query)

    action_output = deepcopy(kwargs)
    translator = str.maketrans('', '', string.punctuation)
    current_objective = '_'.join(
        kwargs['current_objective'].lower().translate(translator).split())
    action_output[f'sql_query_result_for_{current_objective}'] = sql_query_result

    return action_output


def _do_query_sql_database(sql_query: str) -> str:
    """
    Given a list of results, use LLM to generate a response.
    :param sql_query: A list of results collected.
    :return: A string as the response.
    """
    db_path = os.getenv('MOVIELENS_DB_PATH', default='')
    print("Querying from db:", db_path)
    conn = sqlite3.connect(db_path)
    query_result = pd.read_sql_query(sql_query, conn)
    print("Finished querying from:", db_path)
    return json.dumps(query_result.to_json())


def run_example():
    """
    This is an example usage for using _do_query_sql_database to execute a SQL query.
    """
    print(_do_query_sql_database('SELECT * FROM movies LIMIT 5'))
    print(_do_query_sql_database('SELECT * FROM ratings LIMIT 5'))
    print(_do_query_sql_database('SELECT * FROM tags LIMIT 5'))
    print(_do_query_sql_database(
        'SELECT title, MAX(rating) AS best_rating '
        'FROM movies JOIN ratings ON movies.movieId = ratings.movieId '
        'WHERE strftime(\'%Y\', datetime(ratings.timestamp, \'unixepoch\')) = \'2009\' '
        'GROUP BY title ORDER BY best_rating DESC LIMIT 3'))


if __name__ == "__main__":
    run_example()
