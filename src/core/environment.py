import asyncio
from typing import List, Dict, Optional, Set

from src.domain.models.memory.information import Information
from src.utils.environment_utils import get_agent_output_information_name


class Environment:
    _agent_ids: Set[str]
    _information_sources: Dict[str, asyncio.Queue]

    """
    Fields for monitoring the information sources for outputs from an agent.
    """
    _monitor_task: Optional[asyncio.Task]
    _stop_event: Optional[asyncio.Event]

    def __init__(self,
                 agent_ids: Optional[Set[str]] = None,
                 information_names: Optional[List[str]] = None):
        self._agent_ids = agent_ids if agent_ids is not None else set()
        self._information_sources = {}

        self._monitor_task = None
        self._stop_event = None

        if information_names is not None:
            for information_name in information_names:
                self.init_information_source(information_name)

    def __str__(self) -> str:
        return f'''
Environment @ {id(self)}
Registered Agents: {list(self._agent_ids)}
Information Sources: {list(self._information_sources.keys())}
'''

    def register_agent(self, agent_id: str):
        if agent_id in self._agent_ids:
            raise KeyError(f'{agent_id} already exists!')
        self._agent_ids.add(agent_id)

    def init_information_source(self, information_name: str):
        """
        Initialize a new information source.
        """
        self._information_sources[information_name] = asyncio.Queue()

    def get_information_source_by_name(self, information_name: str) -> asyncio.Queue:
        if information_name not in self._information_sources.keys():
            self.init_information_source(information_name)
        return self._information_sources[information_name]

    def get_all_agent_status(self) -> Dict[str, str]:
        """
        Get the status of all agents.
        """
        return {agent_id: 'OK' for agent_id in self._agent_ids}

    async def add_information_to_information_source(self, information_name: str,
                                                    information_val: Information) -> None:
        """
        This allows an agent to add some new information to an information source.
        """
        if information_name not in self._information_sources:
            self.init_information_source(information_name)
        await self._information_sources[information_name].put(information_val)

    async def _monitor(self):
        """
        Monitor all information sources related to agent output asynchronously.
        Print out any agent response if available.
        """
        if self._stop_event is None:
            return
        
        while not self._stop_event.is_set():
            for agent_id in set(self._agent_ids):
                information_name = get_agent_output_information_name(agent_id)
                if information_name in self._information_sources.keys():
                    queue = self._information_sources[information_name]
                    while not queue.empty():
                        info = await queue.get()
                        print(f'Agent {agent_id}: {info.value}')
                        queue.task_done()
            await asyncio.sleep(0.05)

    def start(self):
        if self._monitor_task is None or self._monitor_task.done():
            self._stop_event = asyncio.Event()
            self._monitor_task = asyncio.create_task(self._monitor())

    async def stop(self):
        if self._stop_event and not self._stop_event.is_set():
            print('Stopping environment monitor task...')
            self._stop_event.set()
        if self._monitor_task:
            await self._monitor_task
            self._monitor_task = None
