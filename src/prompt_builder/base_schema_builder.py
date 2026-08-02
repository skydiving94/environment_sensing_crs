from abc import ABC, abstractmethod
from typing import Dict, Any
from src.utils.typed_dicts.information_spec import InformationSpec


class BaseSchemaBuilder(ABC):
    """Abstract interface for translating domain schemas to LLM provider schemas."""

    @abstractmethod
    def build_task_output_tool(self, task_name: str, output_spec: Dict[str, InformationSpec]) -> Dict[str, Any]:
        pass
