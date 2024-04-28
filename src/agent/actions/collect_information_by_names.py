import json
from copy import deepcopy
from typing import Dict, List

from src.memory.information_cache import InformationCache


def do_collect_information_by_names(**kwargs) -> Dict[str, str]:
    information_names_for_response_generation = kwargs['information_names_for_response_generation']

    information_cache: InformationCache = kwargs['information_cache']

    action_output = deepcopy(kwargs)
    action_output['collected_information_for_names'] = (_do_collect_information_by_names(
        information_names_for_response_generation, information_cache))
    return action_output


def _do_collect_information_by_names(
        info_names: List[str],
        information_cache: InformationCache) -> str:
    collected_information_for_names = {}
    for info_name in info_names:
        collected_information_for_names[info_name] = (
            information_cache.get_information_by_name(info_name)[-1].value)
    return json.dumps(collected_information_for_names)
