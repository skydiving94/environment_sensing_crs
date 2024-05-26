from typing import Dict, List

from src.memory.information import Information
from src.memory.information_cache import InformationCache


def do_put_information_into_queue(
        system_prompt: str,
        task_prompt: str,
        information_cache: InformationCache):
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
