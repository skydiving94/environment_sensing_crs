import uuid
from copy import deepcopy
from typing import Collection, List, Dict, Tuple

from src.domain.models.memory.information import Information
from src.domain.enums.information_type import InformationType
from src.core.memory.information_cache import InformationCache
from src.core.memory.long_term_memory import LongTermMemory


class SequentialLongTermMemory(LongTermMemory):
    _short_term_memories: List[InformationCache]
    _memories: Dict[str, Information]
    _metadata: Dict[str, Dict[str, str]]
    _edges: List[Tuple[str, str, str]]

    def __init__(self):
        self._short_term_memories = list()
        self._memories = dict()
        self._metadata = dict()
        self._edges = list()

    def add_short_term_memory(self, short_term_memory: InformationCache) -> None:
        self._short_term_memories.append(deepcopy(short_term_memory))

    def add_memories(self, contents: List[str], **kwargs) -> List[str]:
        metadata_list = kwargs.get('metadata', [])
        edges_list = kwargs.get('edges', [])

        memory_ids = []
        for idx, content in enumerate(contents):
            mem_id = str(uuid.uuid4())

            info = Information(
                raw_value=content,
                name=f"memory_{mem_id}",
                information_type=InformationType.STRING
            )

            self._memories[mem_id] = info
            if idx < len(metadata_list):
                self._metadata[mem_id] = metadata_list[idx]
            else:
                self._metadata[mem_id] = {}

            memory_ids.append(mem_id)

        self._edges.extend(edges_list)
        return memory_ids

    def search_memories(self, query: str, top_k: int, **kwargs) -> List[Information]:
        metadata_filters = kwargs.get('metadata_filters', {})
        results = []

        # Search new generic memories
        for mem_id, info in self._memories.items():
            meta = self._metadata.get(mem_id, {})
            match_meta = all(meta.get(k) == v for k,
                             v in metadata_filters.items())

            if match_meta and (query.lower() in str(info.raw_value).lower() or query == ""):
                results.append(info)

        # Search legacy short term memories (Stopgap for functional parity)
        for stm in self._short_term_memories:
            stm_str = str(stm)
            if query.lower() in stm_str.lower() or query == "":
                # Wrap the legacy cache string in a mock Information object
                results.append(Information(
                    raw_value=stm_str,
                    name="legacy_stm_block",
                    information_type=InformationType.STRING
                ))

        return results[:top_k]

    def get_memory_by_id(self, memory_id: str) -> Information:
        if memory_id in self._memories:
            return self._memories[memory_id]
        raise ValueError(f"Memory ID {memory_id} not found.")

    def get_unique_metadata_values(self, metadata_key: str) -> List[str]:
        values = set()
        for meta in self._metadata.values():
            if metadata_key in meta:
                values.add(meta[metadata_key])
        return list(values)

    def get_related_memories(self, source_memory_id: str, relation_type: str) -> List[Information]:
        related = []
        for src, rel, tgt in self._edges:
            if src == source_memory_id and rel == relation_type:
                if tgt in self._memories:
                    related.append(self._memories[tgt])
        return related
