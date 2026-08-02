import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .llm_client import BaseLLMClient

load_dotenv()


class OpenAILLMClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.default_model = model or os.getenv('OPENAI_TEXT_MODEL', 'gpt-4o')

    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> Any:

        kwargs = {
            "model": model or self.default_model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        if tool_choice:
            kwargs["tool_choice"] = tool_choice

        return await self.client.chat.completions.create(**kwargs)
