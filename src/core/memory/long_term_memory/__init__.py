import abc
from abc import ABC
from typing import Collection, List, Dict, Tuple
from src.domain.models.memory.information import Information
from src.core.memory.information_cache import InformationCache


class LongTermMemory(ABC):
    @abc.abstractmethod
    def add_short_term_memory(self, short_term_memory: InformationCache) -> None:
        pass

    @abc.abstractmethod
    def add_memories(self, contents: List[str], **kwargs) -> List[str]:
        pass

    @abc.abstractmethod
    def search_memories(self, query: str, top_k: int, **kwargs) -> List[Information]:
        pass

    @abc.abstractmethod
    def get_memory_by_id(self, memory_id: str) -> Information:
        pass

    @abc.abstractmethod
    def get_unique_metadata_values(self, metadata_key: str) -> List[str]:
        pass

    @abc.abstractmethod
    def get_related_memories(self, source_memory_id: str, relation_type: str) -> List[Information]:
        pass
