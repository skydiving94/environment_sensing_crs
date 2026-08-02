from src.service.llm.base_client import BaseLLMClient
from src.service.llm.openai_client import OpenAILLMClient


def get_llm_instance(llm_provider: str = 'openai') -> BaseLLMClient:
    provider_clean = llm_provider.strip().lower()
    match provider_clean:
        case 'openai':
            return OpenAILLMClient()
        case _:
            raise ValueError(f'{llm_provider} is not supported.')
