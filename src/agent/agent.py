from typing import List, Tuple, Callable, Any, Optional, Dict

from src.information import Information
from src.interaction_history import InteractionHistory
from src.utils.task_utils import TaskSpec


class Agent:
    agent_id: str
    role_description: str
    action_description_pairs: List[Tuple[Callable[..., Any], Optional[str]]]
    task_specs: List[TaskSpec]

    interaction_history: List[InteractionHistory]
    information_queues: List[Any]  # TODO: The specific type is to be determined later.

    agent_data_file_path: str

    def __init__(self):
        """
        An agent can perform a variety of tasks.
        To begin with, it can interact with a user by listening to their input and talking back to
        them.
        It can also analyze user's input and decide if it needs to perform specific tasks to fulfill
        user's need or perform its duty, as specified by its role description.
        """
        pass

    def listen(self, user_input: str):
        """
        Allows users to communicate in text with the agent.
        :param user_input: A string provided by the user trying to engage with the agent.
        """
        pass

    def _record_interaction(self, content: str, is_user_input):
        """
        Record interaction history.
        :param content: User input or response by the agent.
        :param is_user_input: Whether it is user input.
        """
        pass

    def _write(self):
        """
        Periodically persists agent-related data to perm storage in the file system.
        """
        pass

    def _read(self):
        """
        Read from the file system past agent-related data and re-populate
        related agent state values.
        """
        pass

    def _monitor(self):
        """
        Monitor all registered information sources, which are essentially queues.
        Whenever a new piece of information is available, pick one and process it
        in the round-robin fashion.
        """
        pass

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
        pass

    def _register_information_source(self, information_name: str):
        """
        Register the information source.
        :param information_name: Name of the information source.
        """
        pass

    def _pick_a_task(self, information: Information) -> TaskSpec:
        """
        This is the first thing an agent does when processing a piece of information.
        It decides which task is appropriate to process this piece of information.
        :param information: The information to be processed by the agent.
        :return: The task chosen by the agent.
        """
        pass

    def _execute_a_task(self, task_spec: Dict, arg_key2arg_val: Dict) -> dict:
        """
        This is the second thing an agent does.
        After deciding which task to execute, it executes it based on the task spec.

        :param task_spec:
        :param arg_key2arg_val:
        :return:
        """
        pass

    def _formulate_response(self, results: List[Dict]) -> str:
        pass

    def _talk(self) -> str:
        """
        Talks back to the user given formulated response.
        """
        pass
