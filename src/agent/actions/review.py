from typing import List

from src.typed_dicts.information import Information
from src.typed_dicts.review_result import ReviewResult


def do_review(information_cache: List[Information]) -> ReviewResult:
    raise NotImplementedError


def _do_review(result: dict, task_spec: dict) -> ReviewResult:
    """
    This action corresponds to the task of REVIEW_ACTION_RESULT from another agent.

    :param result: A dict containing data corresponding to the result of the other agent.
    :param task_spec: A dict parsed from the spec of the task executed.
    :return: A ReviewResult dict containing the review result.
    """
    raise NotImplementedError
