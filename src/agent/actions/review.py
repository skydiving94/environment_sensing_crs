from typing import TypedDict


class ReviewResult(TypedDict):
    is_acceptable: bool
    criteria2scoring: dict
    overall_score: float


def do_review(result: dict, task_spec: dict) -> ReviewResult:
    """
    This action corresponds to the task of REVIEW_ACTION_RESULT from another agent.

    :param result: A dict containing data corresponding to the result of the other agent.
    :param task_spec: A dict parsed from the spec of the task executed.
    :return: A ReviewResult dict containing the review result.
    """
    pass
