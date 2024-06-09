import os
from typing import Optional, List

from dotenv import load_dotenv

from src.agent.agent import Agent
from src.environment.environment import Environment
from src.memory.information_cache import InformationCache
from src.memory.information_cache.log_based_task_agnostic_information_cache import \
    LogBasedTaskAgnosticInformationCache
from src.memory.long_term_memory import LongTermMemory
from src.memory.long_term_memory.sequential_long_term_memory import SequentialLongTermMemory

load_dotenv()


class AgentFactory:
    """
    This class is for creating different types of agents sharing the same:
    - code_root_path
    - environment
    - in_information_queue_names
    - out_information_queue_names
    - llm_provider
    Note: environment and information queue names can be left as None, and can be registered to
        each agent one by one.

    Two types of agents are supported at the moment:
    - log_based_agent
    - knowledge_based_agent
    """

    _resource_root_path: str
    _environment: Optional[Environment]
    _in_information_queue_names: Optional[List[str]]
    _out_information_queue_names: Optional[List[str]]
    _llm_provider: str
    _current_objective: Optional[str]

    def __init__(
        self,
        code_root_path: Optional[str] = os.getenv('CODE_ROOT_PATH'),
        environment: Optional[Environment] = None,
        in_information_queue_names: Optional[List[str]] = None,
        out_information_queue_names: Optional[List[str]] = None,
        llm_provider: str = 'openai',
    ):
        if code_root_path is not None:
            self._resource_root_path = os.path.join(code_root_path, 'resources')
        else:
            raise ValueError('CODE_ROOT_PATH is not valid!')

        self._environment = environment
        self._in_information_queue_names = in_information_queue_names
        self._out_information_queue_names = out_information_queue_names
        self._llm_provider = llm_provider

    def create_knowledge_based_agent(
        self,
        agent_id: str,
        role_description: str,
        current_objective: Optional[str] = None
    ):
        raise NotImplementedError
        # return self._create_agent(
        #     agent_id,
        #     role_description,
        #     os.path.join(self._resource_root_path, 'knowledge_based_agent'),
        #     current_objective
        # )

    def create_log_based_agent(
        self,
        agent_id: str,
        role_description: str,
        current_objective: Optional[str] = None,
        is_verbose: bool = False,
        should_output_json: bool = False,
    ):
        return self._create_agent(
            agent_id,
            role_description,
            os.path.join(self._resource_root_path, 'log_based_agent'),
            LogBasedTaskAgnosticInformationCache(),
            SequentialLongTermMemory(),
            current_objective,
            is_verbose,
            should_output_json
        )

    def _create_agent(
        self,
        agent_id: str,
        role_description: str,
        resource_root_path: str,
        information_cache: InformationCache,
        long_term_memory: LongTermMemory,
        current_objective: Optional[str] = None,
        is_verbose: bool = False,
        should_output_json: bool = False
    ):
        return Agent(
            agent_id,
            role_description,
            resource_root_path,
            information_cache,
            long_term_memory,
            self._environment,
            self._in_information_queue_names,
            self._out_information_queue_names,
            self._llm_provider,
            current_objective,
            is_verbose,
            should_output_json
        )
