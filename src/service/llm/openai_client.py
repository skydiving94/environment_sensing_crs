import os
import logging
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI, OpenAIError, RateLimitError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
from .base_client import BaseLLMClient

load_dotenv()
logger = logging.getLogger(__name__)


class OpenAILLMClient(BaseLLMClient):
    """
    Production-ready asynchronous OpenAI client wrapper implementing strict typing,
    Domain-Driven Design boundaries, and robust automatic retry logic with exponential backoff.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        temperature: float = 0.0,
        model: Optional[str] = None,
    ):
        self.model_name = model_name or model or os.getenv(
            "OPENAI_MODEL", "gpt-4o")
        self.temperature = temperature

        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
        resolved_org = organization or os.getenv("OPENAI_ORGANIZATION")

        if not resolved_api_key:
            raise ValueError(
                "OpenAI API key is missing. Set OPENAI_API_KEY in environment or pass it explicitly.")

        self.client = AsyncOpenAI(
            api_key=resolved_api_key,
            organization=resolved_org
        )

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((
            RateLimitError,
            APIConnectionError,
            OpenAIError,
            TimeoutError
        )),
        reraise=True
    )
    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Any] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Executes the OpenAI chat completion call and returns the raw ChatCompletion response object 
        so that OpenAIResponseParser can successfully extract native tool calls and choices.
        Protected by exponential backoff retries on rate limits or network failures.
        """
        call_kwargs: Dict[str, Any] = {
            "model": model or self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }
        if tools:
            call_kwargs["tools"] = tools
        if tool_choice:
            call_kwargs["tool_choice"] = tool_choice

        try:
            response = await self.client.chat.completions.create(**call_kwargs)
            return response
        except Exception as e:
            logger.error(
                f"OpenAILLMClient call failed after retries: {str(e)}")
            raise

    async def generate_structured_response(
        self,
        messages: List[Dict[str, Any]],
        response_format: Any,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Generates a structured response complying with a Pydantic model schema.
        """
        call_kwargs: Dict[str, Any] = {
            "model": model or self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "response_format": response_format,
        }
        try:
            response = await self.client.chat.completions.create(**call_kwargs)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(
                f"OpenAILLMClient structured generation failed: {str(e)}")
            raise
