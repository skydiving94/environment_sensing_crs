from typing import Dict, List

from src.typed_dicts.information import Information


def do_put_information_into_queue(
        system_prompt: str,
        task_prompt: str,
        information_cache: List[Information]):
    raise NotImplementedError


def _do_put_information_into_queue(
        system_prompt: str,
        task_prompt: str,
        information_queue_name: str,
        information_queues: Dict[str, List[Information]]):
    """
    Put information into the specific information queue.
    """
    raise NotImplementedError
