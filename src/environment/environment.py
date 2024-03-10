import threading
from collections import deque
from typing import List, Dict, Optional, Set

from src.utils.environment_utils import get_agent_output_information_name
from src.information_cache.information import Information


class Environment:
    _agent_ids: Set[str]
    # Could be better with priority values.
    _information_sources: Dict[str, deque[Information]]

    """
    Fields for monitoring the information sources for outputs from an agent.
    """
    _monitor_thread: threading.Thread
    _stop_event: threading.Event

    def __init__(self,
                 agent_ids: Optional[Set[str]] = None,
                 information_names: Optional[List[str]] = None):
        self._agent_ids = agent_ids if agent_ids is not None else set()
        self._information_sources = {}

        if information_names is not None:
            for information_name in information_names:
                self.init_information_source(information_name)

        self._start_monitor_thread()

    def __del__(self):
        """
        Destructor is called when an object is destroyed.
        The monitor threads should hence be terminated.
        """
        self._stop_monitor_thread()

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
        :param information_name: The name of the information.
        """
        self._information_sources[information_name] = deque()

    def get_information_source_by_name(self, information_name: str) -> deque[Information]:
        if information_name not in self._information_sources.keys():
            self.init_information_source(information_name)
        return self._information_sources[information_name]

    def get_all_agent_status(self) -> Dict[str, str]:
        """
        Get the status of all agents.
        :return: A dictionary of agent_id to status.
        """
        # TODO: Implement different status for agents,
        #  using information from monitor_thread
        # Note: Maybe we can also move this function, together with the logic of
        # environment_with_one_agent to a new class called Session?
        # A Session would hold an environment and multiple agents.
        # That way we can avoid having circular references?
        return {agent_id: 'OK' for agent_id in self._agent_ids}

    def _monitor(self):
        """
        Monitor all information sources related to agent output.
        Print out any agent response if available.
        """
        while not self._stop_event.is_set():
            for agent_id in self._agent_ids:
                information_name = get_agent_output_information_name(agent_id)
                while len(self._information_sources[information_name]) > 0:
                    print(self._information_sources[information_name][0])
                    self._information_sources[information_name].popleft()

    def _start_monitor_thread(self):
        self._stop_event = threading.Event()

        self._monitor_thread = threading.Thread(target=self._monitor)
        self._monitor_thread.start()

    def _stop_monitor_thread(self):
        print('Stopping monitor thread...')
        self._stop_event.set()
        self._monitor_thread.join()
