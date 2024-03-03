import threading
from collections import deque
from typing import List, Dict, Optional

from src.agent.agent import Agent
from src.typed_dicts.information import Information


class Environment:
    # Somewhat rudimentary. Ideally a graph or network of agents is better?
    _agents: Dict[str, Agent]

    # Could be better with priority values.
    _information_queues: Dict[str, deque[Information]]

    _monitor_thread: threading.Thread
    _stop_event: threading.Event

    def __init__(self,
                 agents: Optional[List[Agent]] = None,
                 information_names: Optional[List[str]] = None):
        self._agents = {}
        self._information_queues = {}

        if agents is not None:
            for agent in agents:
                self.add_agent(agent)

        if information_names is not None:
            for information_name in information_names:
                self.init_information_queue(information_name)

    def __del__(self):
        """
        Destructor is called when an object is destroyed.
        The monitor threads should hence be terminated.
        """
        self._stop_monitor_thread()

    def init_information_queue(self, information_name):
        """
        Initialize a new information queue.
        :param information_name: The name of the information.
        """
        self._information_queues[information_name] = deque()

    def add_agent(self, agent: Agent):
        """
        Add a new agent to the environment.
        :param agent: The agent to be added to the environment.
        :return:
        """
        self._agents[agent.get_agent_id()] = agent
        self.init_information_queue(self._get_agent_output_information_name(agent))

    def talk_to_agent(self, agent_id: str, message: str):
        if agent_id not in self._agents:
            raise LookupError(f'{agent_id} is not a valid agent.')
        else:
            self._agents[agent_id].listen(message)

    @staticmethod
    def _get_agent_output_information_name(agent: Agent) -> str:
        return f'agent_output_{agent.get_agent_id()}'

    def _monitor(self):
        """
        Monitor all information queues related to agent output.
        Print out any agent response if available.
        """
        while not self._stop_event.is_set():
            for agent in self._agents.values():
                information_name = self._get_agent_output_information_name(agent)
                while len(self._information_queues[information_name]) > 0:
                    print(self._information_queues[information_name][0])
                    self._information_queues[information_name].popleft()

    def _start_monitor_thread(self):
        self._monitor_thread = threading.Thread(target=self._monitor)
        self._monitor_thread.start()
        self._stop_event = threading.Event()

    def _stop_monitor_thread(self):
        self._stop_event.set()
        self._monitor_thread.join()