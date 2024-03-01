from typing import List, Dict

from src.typed_dicts.information import Information


def do_formulate_response(
        system_prompt: str,
        task_prompt: str,
        information_cache: List[Information]) -> str:
    raise NotImplementedError


def _do_formulate_response(
        system_prompt: str,
        task_prompt: str,
        results: List[Dict]) -> str:
    """
    Given a list of results, use LLM to generate a response.
    :param results: A list of results collected.
    :return: A string as the response.
    """
    raise NotImplementedError

