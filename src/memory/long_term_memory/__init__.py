import abc
from abc import ABC
from typing import Collection

from src.memory.information import Information
from src.memory.information_cache import InformationCache


class LongTermMemory(ABC):

    @abc.abstractmethod
    def add_short_term_memory(self, short_term_memory: InformationCache):
        pass

    @abc.abstractmethod
    def get_short_term_memories(self) -> Collection[InformationCache]:
        pass

    @abc.abstractmethod
    def retrieve_information_for_context(self, current_objective: str, task_description: str) -> Information:
        pass

    @abc.abstractmethod
    def retrieve_unstructured_information_for_context(self, current_objective, task_description: str) -> str:
        pass

    @abc.abstractmethod
    def retrieve_all_information_as_text(self) -> str:
        pass