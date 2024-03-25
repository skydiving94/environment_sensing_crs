# Query SQL Database action
import json
import sqlite3
from copy import deepcopy
from typing import Dict

import pandas as pd

# TODO: Init this database connection in a better way
conn = sqlite3.connect('/Users/zpeng/project/environment_sensing_crs/dataset/movielens.db')


def do_query_sql_database(**kwargs) -> Dict[str, str]:
    sql_query = kwargs['sql_query']

    sql_query_result = _do_query_sql_database(sql_query)

    action_output = deepcopy(kwargs)

    # FIXME: We might need to add a prefix to the naming of the key so that it does not collide
    #  with the keys from other functions, which can have different key names but different vals.
    action_output['sql_query_result'] = sql_query_result
    return action_output


def _do_query_sql_database(sql_query: str) -> str:
    """
    Given a list of results, use LLM to generate a response.
    :param sql_query: A list of results collected.
    :return: A string as the response.
    """
    query_result = pd.read_sql_query(sql_query, conn)
    return json.dumps(query_result.to_json())


if __name__ == "__main__":
    print(_do_query_sql_database("SELECT * FROM movies LIMIT 5"))
    print(_do_query_sql_database("SELECT * FROM ratings LIMIT 5"))
    print(_do_query_sql_database("SELECT * FROM tags LIMIT 5"))
