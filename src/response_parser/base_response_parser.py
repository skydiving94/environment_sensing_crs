from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseResponseParser(ABC):
    """Abstract interface for extracting usable JSON/Dicts from raw LLM provider responses."""

    @abstractmethod
    def extract_json_from_tool_call(self, raw_llm_response: Any) -> Dict[str, Any]:
        pass
