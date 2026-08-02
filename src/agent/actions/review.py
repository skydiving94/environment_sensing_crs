from typing import List

from src.memory.information_cache import InformationCache
from src.utils.typed_dicts.review_result import ReviewResult
from src.agent.actions import action_tool


@action_tool(name="do_review")
def do_review(
        system_prompt: str,
        task_prompt: str,
        information_cache: InformationCache) -> ReviewResult:
    """
    Review the action result from another agent based on the provided system and task prompts.
    """
    raise NotImplementedError


def _do_review(system_prompt: str, task_prompt: str, result: dict, task_spec: dict) -> ReviewResult:
    """
    This action corresponds to the task of REVIEW_ACTION_RESULT from another agent.

    :param result: A dict containing data corresponding to the result of the other agent.
    :param task_spec: A dict parsed from the spec of the task executed.
    :return: A ReviewResult dict containing the review result.
    """
    raise NotImplementedError
