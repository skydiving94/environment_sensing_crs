import os
from typing import Tuple, List, Dict


def get_task_spec_path_by_name(task_spec_name: str) -> str:
    return get_all_task_spec_paths()[task_spec_name]


def get_all_task_spec_paths() -> Dict[str, str]:
    """
    Return a map of task name to their paths corresponding to the latest version v[n].json
     under the resource directory programmatically.
    """
    # Read task specs from .env
    task_spec_paths = {
        'draw_more_info': os.getenv('TASK_SPEC_FOR_DRAW_MORE_INFO_PATH', default=''),
        'pick_a_task': os.getenv('TASK_SPEC_FOR_PICK_A_TASK', default=''),
        'generate_sql': os.getenv('TASK_SPEC_FOR_GENERATE_SQL', default=''),
        'query_sql': os.getenv('TASK_SPEC_FOR_QUERY_SQL', default=''),
        'formulate_response': os.getenv('TASK_SPEC_FOR_FORMULATE_RESPONSE', default=''),
        'prepare_formulate_response':
            os.getenv('TASK_SPEC_FOR_DECIDE_INFO_FOR_PREPARE_FORMULATE_RESPONSE', default=''),
    }
    return task_spec_paths


def get_all_available_task_name_description_pairs() -> List[Tuple[str, str]]:
    """
    Fetch all defined tasks under resources/task_specs/[task_name]/v[n].json
    and return their name and description.
    """
    # FIXME: Implement the actual functionality so it can load dynamically!
    # Maybe we can read from task_specs:description?
    task_name_description_pairs: List[Tuple[str, str]] = [
        # FIXME: Remove determine_user_disposition and pick_a_task, which are predefined
        #   for an agent, irrelevant to the actual need of a user. That is, these tasks are
        #   a priori to any user interactions.
        (
            'determine_user_disposition',
            'The agent should determine if the user is satisfied with its response',
        ),
        (
            'pick_a_task',
            'The agent should decide which task it should execute given existing information.'
        ),
        (
            'generate_sql',
            'The agent should understand user\'s request and '
            'generate SQL query to fetch the required data.'
        ),
        (
            'query_sql',
            'This task execute SQL. Not a LLM task'
        ),
        (
            'prepare_formulate_response',
            'This task determines which information names in the current memory are most relevant '
            'to the objective at hand for generating a response'
        ),
        (
            'formulate_response',
            'This task generates a response to user using collected information suggested by '
            '"prepare_formulate_response" and current objective and hence '
            'should be utilized after "prepare_formulate_response" has been executed first.'
        ),
        (
            'draw_more_info',
            'The agent should keep drawing more information as the existing one is not '
            'sufficient to make a decision on.'
        ),
    ]

    return task_name_description_pairs


def get_stringified_all_available_task_name_description_pairs() -> str:
    task_name_description_pairs = get_all_available_task_name_description_pairs()
    s = ''
    for name, description in task_name_description_pairs:
        s += f'TASK_NAME: {name}\nTASK_DESCRIPTION: {description}\n***************\n'
    return s
