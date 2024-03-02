from typing import Dict, List

from src.utils.typed_dicts.information import Information


def do_draw_information_from_queue(
        system_prompt: str,
        task_prompt: str,
        information_cache: List[Information]):
    raise NotImplementedError


def _do_draw_information_from_queue(
        system_prompt: str,
        task_prompt: str,
        information_queues: Dict[str, List[Information]],
        information_cache: List[Information]):
    """
    Draw information from the specific information queue and add the drawn information to the cache.
    """
    raise NotImplementedError
