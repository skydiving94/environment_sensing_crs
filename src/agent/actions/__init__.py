from typing import Callable, Any, Tuple, Optional, Dict

from src.agent.actions.collect_information_by_names import do_collect_information_by_names
from src.agent.actions.query_sql_database import do_query_sql_database


def get_all_available_action_data() -> Dict[str, Tuple[Optional[str], Callable[..., Any]]]:
    """
    Fetch all functions with names starting as do_*, together with their doc string
    descriptions.
    :return: A dict that maps name of the action to the optional description of the action,
    and the actual function.
    """

    # FIXME: Implement this function! Load all actions from actions directory.
    return {
        'do_query_sql_database': ('execute a SQL query', do_query_sql_database),
        'do_collect_information_by_names':
            ('Collect all information by information names', do_collect_information_by_names)
    }
