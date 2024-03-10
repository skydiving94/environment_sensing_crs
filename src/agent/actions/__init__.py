from typing import Callable, Any, Tuple, Optional, Dict


def get_all_available_action_data() -> Dict[str, Tuple[Optional[str], Callable[..., Any]]]:
    """
    Fetch all functions with names starting as do_*, together with their doc string
    descriptions.
    :return: A dict that maps name of the action to the optional description of the action,
    and the actual function.
    """

    # TODO: Implement this function!
    return {}
