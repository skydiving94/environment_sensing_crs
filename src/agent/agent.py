from typing import List, Tuple, Callable, Any, Optional, Dict

from src.agent.actions import get_all_available_action_description_pairs
from src.typed_dicts.information import Information
from src.typed_dicts.interaction_history import InteractionHistory
from src.typed_dicts.task_spec import TaskSpec


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
    _in_information_queues: Dict[str, List[Information]]
    _out_information_queues: Dict[str, List[Information]]

    _agent_data_file_path: str

    """
    Constructor
    """

    def __init__(self):
        """
        An agent can perform a variety of tasks.
        To begin with, it can interact with a user by listening to their input and talking back to
        them.
        It can also analyze user's input and decide if it needs to perform specific tasks to fulfill
        user's need or perform its duty, as specified by its role description.
        """
        raise NotImplementedError

    """
    Public methods as the way user/environment can interact with an agent. 
    """

    def listen(self, user_input: str):
        """
        Allows users to communicate in text with the agent.
        :param user_input: A string provided by the user trying to engage with the agent.
        """
        raise NotImplementedError

    def see(self, environment_image_path: str):
        """
        Allows the agent to be shown specific useful environmental information.
        :param environment_image_path: The path to the environment image.
        """
        raise NotImplementedError

    def register_information_source(self, information_source_name: str):
        """
        Register the information source.
        :param information_source_name: Name of the information source.
        """
        self._register_information_source(information_source_name)

    def get_agent_id(self):
        return self._agent_id

    """
    Private methods representing the internal capabilities of an agent.
    """

    def _register_information_source(self, information_source_name: str):
        """
        Register the information source.
        :param information_source_name: Name of the information source.
        """
        raise NotImplementedError

    def _monitor(self):
        """
        Monitor all registered information sources, which are essentially queues.
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

    def _record_interaction(self, content: str, is_user_input):
        """
        Record interaction history.
        :param content: User input or response by the agent.
        :param is_user_input: Whether it is user input.
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

    def _talk(self) -> str:
        """
        Talks back to the user given formulated response.
        """
        raise NotImplementedError

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
