import json
from typing import Dict, Any
from .base_response_parser import BaseResponseParser


class OpenAIResponseParser(BaseResponseParser):
    def extract_json_from_tool_call(self, raw_llm_response: Any) -> Dict[str, Any]:
        """Safely navigates the OpenAI AsyncOpenAI response object to extract tool arguments."""
        try:
            tool_call = raw_llm_response.choices[0].message.tool_calls[0]
            return json.loads(tool_call.function.arguments)
        except (IndexError, AttributeError, json.JSONDecodeError) as e:
            # In a robust system, you might want to raise a custom Domain error here
            # to trigger an Agent retry loop.
            raise ValueError(f"Failed to parse OpenAI tool call response: {e}")
