import os
import threading
from collections import deque
from typing import List, Tuple, Callable, Any, Optional, Dict

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from src.agent.actions import get_all_available_action_data
from src.environment.environment import Environment
from src.information_cache.information import Information
from src.information_cache.information_cache import InformationCache
from src.llm import get_llm_instance
from src.task import get_stringified_all_available_task_name_description_pairs, \
    get_task_spec_path_by_name
from src.task.task_spec import TaskSpec
from src.utils.environment_utils import get_agent_output_information_name
from src.utils.typed_dicts.interaction_history import InteractionHistory

load_dotenv()

"""
Keys of special, reserved information names. 
"""
USER_INPUT_INFO_QUEUE_NAME = 'user_input'

AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE = 'current_objective'
AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES = 'information_queue_names'
AGENT_SPECIFIC_INFO_CACHE = 'information_cache'
ALL_POSSIBLE_TASKS = 'all_possible_tasks'
SPECIAL_INFORMATION_NAME_KEYS = [
    AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE,
    AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES,
    AGENT_SPECIFIC_INFO_CACHE,
    ALL_POSSIBLE_TASKS,
]
MAX_DEPTH = 3


class Agent:
    """
    Agent config-related attributes.
    """
    _agent_id: str
    _role_description: str
    _action_description_pairs: Dict[str, Tuple[Optional[str], Callable[..., Any]]]
    _task_specs: List[TaskSpec]
    _llm_instance: BaseChatModel

    """
    Useful data for making decisions.
    """
    _current_objective: List[str]
    # A list of task names being already executed for this objective.
    _task_history: List[str]
    # A collection of information to be processed at once.
    _information_cache: InformationCache

    _interaction_history: List[InteractionHistory]

    _is_process_finished: bool
    # TODO: We need to decide if we should just use a regular queue or a priority queue.

    _environment: Optional[Environment]
    _in_information_queues: Dict[str, Optional[deque[Information]]]
    _out_information_queues: Dict[str, Optional[deque[Information]]]

    _agent_data_file_path: str

    """
    Fields for monitoring the information sources for outputs from an agent.
    """
    _monitor_thread: threading.Thread
    _stop_event: threading.Event

    """
    Constructor
    """

    def __init__(self,
                 agent_id: str,
                 role_description: str,
                 environment: Optional[Environment] = None,
                 in_information_queue_names: Optional[List[str]] = None,
                 out_information_queue_names: Optional[List[str]] = None,
                 llm_provider: str = 'openai'):
        """
        An agent can perform a variety of tasks.
        To begin with, it can interact with a user by listening to their input and talking back to
        them.
        It can also analyze user's input and decide if it needs to perform specific tasks to fulfill
        user's need or perform its duty, as specified by its role description.
        """

        self._agent_id = agent_id
        self._role_description = role_description
        self._llm_instance = get_llm_instance(llm_provider)

        # TODO: Replace the following dicts with an ADT called InformationQueue
        #  which is based on a combination of map and priority queue.
        #  Each information queue has its priority, and each information within a queue also has its
        #  priority.
        self._in_information_queues = dict()
        self._out_information_queues = dict()
        self._current_objective = []

        self.register_environment(environment)
        if in_information_queue_names is not None:
            for information_queue_name in in_information_queue_names:
                self.register_information_queue(information_queue_name, True)
        if out_information_queue_names is not None:
            for information_queue_name in out_information_queue_names:
                self.register_information_queue(information_queue_name, False)

        # This information queue is independent of the environment.
        self._in_information_queues[USER_INPUT_INFO_QUEUE_NAME] = deque()

        self._information_cache = InformationCache()
        self._is_process_finished = False

        # TODO: Finish initializing all other fields!

        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._monitor_thread = threading.Thread(target=self._monitor)
        self._start_monitor_thread()
        pass

    def __del__(self):
        self._stop_monitor_thread()

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
        user_input_queue = self._in_information_queues[USER_INPUT_INFO_QUEUE_NAME]
        if user_input_queue is not None:
            user_input_queue.append(Information(input_message, name=USER_INPUT_INFO_QUEUE_NAME))

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
            if self._environment is None:
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
                    self._environment.get_information_source_by_name(information_queue_name)
            else:
                self._in_information_queues[information_queue_name] = None
        else:
            if self._environment is not None:
                self._out_information_queues[information_queue_name] = \
                    self._environment.get_information_source_by_name(information_queue_name)
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
        while not self._stop_event.is_set():
            # TODO: Replace the following loop with self._in_information_queues.getNext()
            #  once InformationQueue is implemented.
            for information_name in list(self._in_information_queues.keys()):
                if len(self._in_information_queues[information_name]) > 0:
                    information = self._in_information_queues[information_name].popleft()
                    print(f'New information found in {information_name}: {information.value}')

                    # Add the new information to the info cache.
                    self._information_cache.add_information(information)

                    # Pass the new information to process.
                    self._process(information)

    def _process(self, information: Information, depth: int = 0):
        """
        Process a given information drawn from one of the queue being monitored.
        The monitor function is suspended when an information is being processed.
        The process function can draw more information from the information queues if the agent
        decides that it needs more information.

        :param information: An Information typed dict containing the type of the information,
            and the actual data.
        :return:
        """
        if depth >= MAX_DEPTH:
            print('Hmm. There seems to be something wrong with your request. Please try again.')
            self._is_process_finished = True
            return
        print(f'Processing information: {information.value} at depth {depth}')
        self._pause_monitor_thread()

        # Step 1. Given the latest information passed to process and existing information
        # in the information cache, it first picks a task.
        task_spec_for_picked_task = self._pick_a_task()

        if task_spec_for_picked_task is None:
            self._process(information, depth + 1)

        # Step 2. Execute the task given the spec.
        task_output = self._execute_a_task(task_spec_for_picked_task)  # type: ignore
        print(f'task_output from processing at depth {depth}: {task_output}')
        # task_output may have some more meaningful use.

        # Step 3. Check if more processing is needed.
        if self._is_process_finished:
            self._resume_monitor_thread()
            return
        else:
            self._process(information, depth + 1)

    def _pick_a_task(self) -> Optional[TaskSpec]:
        """
        This is the first thing an agent does when processing a piece of information.
        It decides which task is appropriate to process this piece of information.
        :return: The task chosen by the agent.
        """

        task_spec = TaskSpec(task_spec_path=os.getenv('TASK_SPEC_FOR_PICK_A_TASK'))
        result = self._execute_a_task(task_spec)
        if 'task_name' not in result or 'reasoning' not in result:
            return None
        task_name = result['task_name'].value
        reasoning = result['reasoning'].value
        print(f'Task picked: {task_name}')
        print(f'Reasoning: {reasoning}')
        return TaskSpec(task_spec_path=get_task_spec_path_by_name(task_name))

    def _execute_a_task(self, task_spec: TaskSpec) -> Dict:
        """
        This is the second thing an agent does.
        After deciding which task to execute, it executes it based on the task spec.

        :param task_spec:
        :return: A dict containing the task result.
        """

        # Step 0. Check if it belongs to one of the hard-coded actions such as _talk, etc.
        # TODO: Implement this logic later.
        task_name = task_spec.name
        print(f'Executing task: {task_name}')

        # Step 1. Build arg_key_to_arg_val based on input information names and the available
        # data the agent has.
        arg_key_to_arg_val = self._build_arg_key_to_arg_val(task_spec.input_information_names)

        # Step 2. Execute all actions for the task.
        action_names = task_spec.action_names
        action_output = self._execute_actions(action_names, arg_key_to_arg_val)

        # Step 3. Build prompt_key_to_val based on current information stored.
        prompt_key_to_val = self._build_prompt_key_to_val()
        if action_output is not None and len(action_names) > 0:
            prompt_key_to_val['action_output'] = str(action_output)

        # Step 4. Get an instance of the task given the contextual information the agent
        # current has, including the result of the action taken.
        task_instance = task_spec.build_task_instance(prompt_key_to_val)

        # Step 5. Trigger the task instance by invoking the llm instance.
        informations = task_instance.run(self._llm_instance)

        print('Saving the following information to cache...')
        for information_name, information in informations.items():
            print(information)
            self._information_cache.add_information(information)

        # Step 6. Check if this task is a terminating task. i.e. no more processing is needed.
        self._is_process_finished = task_spec.is_terminating_task

        return informations

    @staticmethod
    def _execute_actions(action_names: List[str], arg_key_to_arg_val: Dict) -> Optional[Dict]:
        """
        Execute a pipeline of actions given the initial arg_key_to_arg_val.
        """

        if len(action_names) == 0:
            return None

        print(f'Executing a pipeline of actions: {action_names}')
        available_action_data = get_all_available_action_data()
        action_output: Optional[Dict] = arg_key_to_arg_val
        are_actions_interrupted = False
        for action_name in action_names:
            if action_name not in available_action_data.keys():
                are_actions_interrupted = True
                break
            action_func = available_action_data[action_name][1]
            if action_output is None:
                are_actions_interrupted = True
                break
            action_output = action_func(**action_output)
        if are_actions_interrupted:
            action_output = None
        return action_output

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
            out_information_queue.append(Information(out_message))
        else:
            print('No output information queue is set up.')

    def _clear_objective(self):
        self._current_objective = []
        self._task_history = []
        self._information_cache = InformationCache()

        # Also, reset the priorities for all information sources to default value.

    # A placeholder for a future action which allows an agent to define and name its own action
    #   and have the action stored in the proper path of the file system. After the definition,
    #   the action should trigger also _load_action_description_pairs to make the action ready.

    """
    Methods for setting up an agent or to update an agent.
    """

    def _load_action_description_pairs(self):
        self._action_description_pairs = get_all_available_action_data()

    def _get_special_information_key_to_val(self) -> Dict[str, str]:
        return {
            AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE:
                self._current_objective[0] if len(self._current_objective) > 0 else 'None',
            AGENT_SPECIFIC_INFO_CACHE: self._information_cache.get_information_names_str(),
            AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES:
                str(list(self._in_information_queues.keys())),
            ALL_POSSIBLE_TASKS: get_stringified_all_available_task_name_description_pairs()
        }

    def _build_arg_key_to_arg_val(self, input_information_names: List[str]) -> Dict:
        """
        Build arg_key2arg_val based on input information names and the available
        data the agent has.
        """
        # TODO: Replace the following placeholder return.
        return {}

    def _build_prompt_key_to_val(self) -> Dict[str, str]:
        prompt_key_to_val = self._get_special_information_key_to_val()
        informations = self._information_cache.get_informations()
        for key in informations.keys():
            prompt_key_to_val[key] = (
                ' '.join([information.raw_value for information in informations[key]]))
        return prompt_key_to_val

    def _start_monitor_thread(self):
        self._monitor_thread.start()
        self._pause_event.set()

    def _stop_monitor_thread(self):
        self._stop_event.set()
        self._resume_monitor_thread()
        self._monitor_thread.join()
        print(f'Stopped monitor thread for agent {id(self)}...')

    def _pause_monitor_thread(self):
        self._pause_event.clear()

    def _resume_monitor_thread(self):
        self._pause_event.set()
