from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> Any:
        pass
