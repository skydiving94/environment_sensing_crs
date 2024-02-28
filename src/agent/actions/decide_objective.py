from typing import List

from src.typed_dicts.information import Information
from src.typed_dicts.review_result import ReviewResult


def do_decide_objective(information_cache: List[Information]):
    raise NotImplementedError


def _do_decide_objective(user_input: str, current_objective: List[str]):
    """
    This action is to generate an objective for the agent given user's input.

    :param user_input: The input provided by the user.
    """
    raise NotImplementedError
