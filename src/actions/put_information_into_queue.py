from typing import Dict, List

from src.domain.models.memory.information import Information
from src.core.memory.information_cache import InformationCache
from src.actions import action_tool


@action_tool(name="do_put_information_into_queue")
def do_put_information_into_queue(
        system_prompt: str,
        task_prompt: str,
        information_cache: InformationCache):
    """
    Put information into the specific information queue.
    """
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
