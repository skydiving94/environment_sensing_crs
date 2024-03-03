from collections import deque
from typing import List, Tuple, Callable, Any, Optional, Dict

from src.agent.actions import get_all_available_action_description_pairs
from src.environment.environment import Environment
from src.typed_dicts.information import Information
from src.typed_dicts.interaction_history import InteractionHistory
from src.typed_dicts.task_spec import TaskSpec
from src.utils.environment_utils import get_agent_output_information_name


class Agent:
    """
    Agent config-related attributes.
    """
    _agent_id: str
    _role_description: str
    _action_description_pairs: List[Tuple[Callable[..., Any], Optional[str]]]
    _task_specs: List[TaskSpec]

    """
    Useful data for making decisions.
    """
    _current_objective: List[str]
    # A list of task names being already executed for this objective.
    _task_history: List[str]
    # A collection of information to be processed at once.
    _information_cache: List[Information]

    _interaction_history: List[InteractionHistory]
    # TODO: We need to decide if we should just use a regular queue or a priority queue.

    _environment: Optional[Environment]
    _in_information_queues: Dict[str, Optional[deque[Information]]]
    _out_information_queues: Dict[str, Optional[deque[Information]]]

    _agent_data_file_path: str

    """
    Constructor
    """

    def __init__(self,
                 agent_id: str,
                 role_description: str,
                 environment: Optional[Environment] = None,
                 in_information_queue_names: Optional[List[str]] = None,
                 out_information_queue_names: Optional[List[str]] = None):
        """
        An agent can perform a variety of tasks.
        To begin with, it can interact with a user by listening to their input and talking back to
        them.
        It can also analyze user's input and decide if it needs to perform specific tasks to fulfill
        user's need or perform its duty, as specified by its role description.
        """

        self._agent_id = agent_id
        self._role_description = role_description
        self._in_information_queues = dict()
        self._out_information_queues = dict()

        self.register_environment(environment)
        if in_information_queue_names is not None:
            for information_queue_name in in_information_queue_names:
                self.register_information_queue(information_queue_name, True)
        if out_information_queue_names is not None:
            for information_queue_name in out_information_queue_names:
                self.register_information_queue(information_queue_name, False)

        # TODO: Finish initializing all other fields!
        pass

    """
    Public methods as the way user/environment can interact with an agent. 
    """

    def listen(self, input_message: str):
        """
        Allows users to communicate in text with the agent.
        :param input_message: A string provided by the user trying to engage with the agent.
        """
        # TODO: Replace the mock implementation with actual functionality!
        # Mock implementation to test agent working in an environment.
        # Call talk directly and repeat user's input.
        self._talk(f'User said and I repeat: {input_message}')

    def see(self, environment_image_path: str):
        """
        Allows the agent to be shown specific useful environmental information.
        :param environment_image_path: The path to the environment image.
        """
        raise NotImplementedError

    def register_environment(self, environment: Optional[Environment]):
        """
        Register the agent to its environment.
        :param environment: The environment where an agent is bound to.
        """
        if environment is not None:
            self._environment = environment
            self._environment.register_agent(self._agent_id)
            self.register_information_queue(get_agent_output_information_name(self._agent_id),
                                            False)
        else:
            self._environment = None

    def register_information_queue(self, information_queue_name: str, is_incoming: bool = True):
        """
        Register the information queue.
        :param information_queue_name: Name of the information queue.
        :param is_incoming: Whether it is for in or out information queue.
        """
        if is_incoming:
            if self._environment is not None:
                self._in_information_queues[information_queue_name] = \
                    self._environment.get_information_queue_by_name(information_queue_name)
            else:
                self._in_information_queues[information_queue_name] = None
        else:
            if self._environment is not None:
                self._out_information_queues[information_queue_name] = \
                    self._environment.get_information_queue_by_name(information_queue_name)
            else:
                self._out_information_queues[information_queue_name] = None

    def get_agent_id(self):
        return self._agent_id

    """
    Private methods representing the internal capabilities of an agent.
    """

    def _monitor(self):
        """
        Monitor all registered information queues, which are essentially queues.
        Whenever a new piece of information is available, pick one and process it
        in the round-robin fashion.
        """
        raise NotImplementedError

    def _process(self, information: Information) -> str:
        """
        Process a given information drawn from one of the queue being monitored.
        The monitor function is suspended when an information is being processed.
        The process function can draw more information from the information queues if the agent
        decides that it needs more information.

        :param information: An Information typed dict containing the type of the information,
            and the actual data.
        :return:
        """
        raise NotImplementedError

    def _pick_a_task(self, information: Information) -> TaskSpec:
        """
        This is the first thing an agent does when processing a piece of information.
        It decides which task is appropriate to process this piece of information.
        :param information: The information to be processed by the agent.
        :return: The task chosen by the agent.
        """
        raise NotImplementedError

    def _execute_a_task(self, task_spec: Dict, arg_key2arg_val: Dict) -> dict:
        """
        This is the second thing an agent does.
        After deciding which task to execute, it executes it based on the task spec.

        :param task_spec:
        :param arg_key2arg_val:
        :return: A dict containing the task result.
        """
        raise NotImplementedError

    """
    Hard-coded tasks that is shared by all agents. 
    """

    def _record_interaction(self, content: str, is_input_message):
        """
        Record interaction history.
        :param content: User input or response by the agent.
        :param is_input_message: Whether it is user input.
        """
        raise NotImplementedError

    def _write(self):
        """
        Periodically persists agent-related data to perm storage in the file system.
        """
        raise NotImplementedError

    def _read(self):
        """
        Read from the file system past agent-related data and re-populate
        related agent state values.
        """
        raise NotImplementedError

    def _talk(self, out_message: str):
        """
        Talks back to the user given formulated response.
        """
        out_information_queue = (
            self._out_information_queues)[get_agent_output_information_name(self._agent_id)]
        if out_information_queue is not None:
            out_information_queue.append(Information(value=out_message))
        else:
            print('No output information queue is set up.')

    def _clear_objective(self):
        self._current_objective = []
        self._task_history = []
        self._information_cache = []

    # A placeholder for a future action which allows an agent to define and name its own action
    #   and have the action stored in the proper path of the file system. After the definition,
    #   the action should trigger also _load_action_description_pairs to make the action ready.

    """
    Methods for setting up an agent or to update an agent.
    """

    def _load_action_description_pairs(self):
        self._action_description_pairs = get_all_available_action_description_pairs()

    def _repopulate_information_queues(self, is_incoming: bool = True):
        """
        Register the agent to the information queue in the corresponding environment.
        :param is_incoming: Whether this is an in or out information queue.
        """
        if is_incoming:
            for information_queue_name in self._in_information_queues.keys():
                self.register_information_queue(information_queue_name)
        else:
            for information_queue_name in self._out_information_queues.keys():
                self.register_information_queue(information_queue_name)
