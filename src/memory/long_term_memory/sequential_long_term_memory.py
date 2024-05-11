from copy import deepcopy
from typing import Collection, List

from src.memory.information import Information
from src.memory.information_cache import InformationCache
from src.memory.long_term_memory import LongTermMemory


class SequentialLongTermMemory(LongTermMemory):
    _short_term_memories: List[InformationCache]

    def __init__(self):
        self._short_term_memories = list()

    def add_short_term_memory(self, short_term_memory: InformationCache):
        self._short_term_memories.append(deepcopy(short_term_memory))

    def get_short_term_memories(self) -> Collection[InformationCache]:
        return self._short_term_memories

    def retrieve_information_for_context(self, current_objective: str, task_description: str) -> Information:
        raise NotImplementedError

    def retrieve_unstructured_information_for_context(self, current_objective, task_description: str) -> str:
        raise NotImplementedError

    def retrieve_all_information_as_text(self) -> str:
        information_texts = []
        for idx, short_term_memory in enumerate(self._short_term_memories):
            information_texts.append(f'Information Group {idx}:\n{short_term_memory}')
        return '\n'.join(information_texts)
