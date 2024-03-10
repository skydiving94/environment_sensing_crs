from typing import Tuple, List, Dict


def get_task_spec_path_by_name(task_spec_name: str) -> str:
    return get_all_task_spec_paths()[task_spec_name]


def get_all_task_spec_paths() -> Dict[str, str]:
    """
    Return a map of task name to their paths corresponding to the latest version v[n].json
     under the resource directory programmatically.
    """
    task_spec_paths = {
        'draw_more_info': '/Users/timowang/Developer/environment_sensing_crs/'
                          'resources/task_specs/draw_more_info/v0.json',
        'pick_a_task': '/Users/timowang/Developer/environment_sensing_crs/'
                       'resources/task_specs/pick_a_task/v0.json',
    }
    return task_spec_paths


def get_all_available_task_name_description_pairs() -> List[Tuple[str, str]]:
    """
    Fetch all defined tasks under resources/task_specs/[task_name]/v[n].json
    and return their name and description.
    """
    # FIXME: Implement the actual functionality so it can load dynamically!
    task_name_description_pairs: List[Tuple[str, str]] = [
        (
            'draw_more_info',
            'The agent should keep drawing more information as the existing one is not '
            'sufficient to make a decision on.'
        ),
        (
            'pick_a_task',
            'The agent should decide which task it should execute given existing information.'
        ),
    ]

    return task_name_description_pairs


def get_stringified_all_available_task_name_description_pairs() -> str:
    task_name_description_pairs = get_all_available_task_name_description_pairs()
    s = ''
    for name, description in task_name_description_pairs:
        s += f'TASK_NAME: {name}\nTASK_DESCRIPTION: {description}\n***************\n'
    return s
