from typing import List

from src.utils.typed_dicts import Information


def do_decide_objective(
        system_prompt: str,
        task_prompt: str,
        information_cache: List[Information]) -> str:
    raise NotImplementedError


def _do_decide_objective(
        system_prompt: str,
        task_prompt: str,
        user_input: str,
        current_objective: List[str]) -> str:
    """
    This action is to generate an objective for the agent given user's input.

    :param user_input: The input provided by the user.
    """
    raise NotImplementedError
