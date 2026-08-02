import os
from typing import Optional, List

from dotenv import load_dotenv

from src.core.agent import Agent
from src.core.environment import Environment
from src.core.memory.information_cache import InformationCache
from src.core.memory.information_cache.log_based_task_agnostic_information_cache import \
    LogBasedTaskAgnosticInformationCache
from src.core.memory.long_term_memory import LongTermMemory
from src.core.memory.long_term_memory.sequential_long_term_memory import SequentialLongTermMemory

from src.service.llm.base_client import BaseLLMClient
from src.service.llm.openai_client import OpenAILLMClient

from src.adapters.prompt_builder.base_schema_builder import BaseSchemaBuilder
from src.adapters.prompt_builder.openai_schema_builder import OpenAISchemaBuilder
from src.adapters.response_parser.base_response_parser import BaseResponseParser
from src.adapters.response_parser.openai_response_parser import OpenAIResponseParser

load_dotenv()

MEMORY_MANAGEMENT_INSTRUCTION = (
    "\n\n[SYSTEM OS CAPABILITIES: AUTONOMOUS MEMORY MANAGEMENT]\n"
    "You are an AI agent with a persistent, tiered memory architecture. Your active context window is limited. "
    "You MUST actively manage your own memory state using your available tools:\n"
    "1. write_to_cache: Use this tool to save extracted facts, user preferences, or vital data to your active Core Memory. "
    "If you do not explicitly save important information, you will forget it in future turns.\n"
    "2. search_long_term_memory: If you lack the context to answer a query, use this tool to search your historical archives."
)


class AgentFactory:
    """
    This class is for creating different types of agents sharing the same:
    - code_root_path
    - environment
    - in_information_queue_names
    - out_information_queue_names
    - llm_provider
    """

    _resource_root_path: str
    _environment: Optional[Environment]
    _in_information_queue_names: Optional[List[str]]
    _out_information_queue_names: Optional[List[str]]

    # The concrete dependencies to be injected into agents
    _llm_client: BaseLLMClient
    _schema_builder: BaseSchemaBuilder
    _response_parser: BaseResponseParser

    def __init__(
        self,
        code_root_path: Optional[str] = os.getenv('CODE_ROOT_PATH'),
        environment: Optional[Environment] = None,
        in_information_queue_names: Optional[List[str]] = None,
        out_information_queue_names: Optional[List[str]] = None,
        llm_provider: str = 'openai',
    ):
        if code_root_path is not None:
            self._resource_root_path = os.path.join(
                code_root_path, 'resources')
        else:
            raise ValueError('CODE_ROOT_PATH is not valid!')

        self._environment = environment
        self._in_information_queue_names = in_information_queue_names
        self._out_information_queue_names = out_information_queue_names

        provider_clean = llm_provider.strip().lower()

        # DI Container: Instantiate the correct platform-specific tools once
        if provider_clean == 'openai':
            self._llm_client = OpenAILLMClient()
            self._schema_builder = OpenAISchemaBuilder()
            self._response_parser = OpenAIResponseParser()
        else:
            raise ValueError(
                f"LLM Provider '{llm_provider}' is not supported.")

    def create_knowledge_based_agent(
        self,
        agent_id: str,
        role_description: str,
        current_objective: Optional[str] = None
    ):
        raise NotImplementedError

    def create_log_based_agent(
        self,
        agent_id: str,
        role_description: str,
        current_objective: Optional[str] = None,
        is_verbose: bool = False,
    ):
        return self._create_agent(
            agent_id,
            role_description,
            os.path.join(self._resource_root_path, 'log_based_agent'),
            LogBasedTaskAgnosticInformationCache(),
            SequentialLongTermMemory(),
            current_objective,
            is_verbose
        )

    def _create_agent(
        self,
        agent_id: str,
        role_description: str,
        resource_root_path: str,
        information_cache: InformationCache,
        long_term_memory: LongTermMemory,
        current_objective: Optional[str] = None,
        is_verbose: bool = False
    ):
        augmented_role_description = f"{role_description}\n{MEMORY_MANAGEMENT_INSTRUCTION}"
        return Agent(
            agent_id=agent_id,
            role_description=augmented_role_description,
            resource_root_path=resource_root_path,
            information_cache=information_cache,
            long_term_memory=long_term_memory,

            # Inject the interfaces, not the raw string
            llm_client=self._llm_client,
            schema_builder=self._schema_builder,
            response_parser=self._response_parser,

            environment=self._environment,
            in_information_queue_names=self._in_information_queue_names,
            out_information_queue_names=self._out_information_queue_names,
            current_objective=current_objective,
            is_verbose=is_verbose
        )
