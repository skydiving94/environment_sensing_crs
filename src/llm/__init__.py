from src.llm.openai import openai_llm


def get_llm_instance(llm_provider: str = 'openai'):
    match llm_provider:
        case 'openai':
            return openai_llm
        case _:
            raise ValueError(f'{llm_provider} is not supported.')
