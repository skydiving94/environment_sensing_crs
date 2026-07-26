import os
import asyncio
import time
from typing import List, Tuple, Callable, Any, Optional, Dict

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from src.agent.actions import get_all_available_action_data
from src.environment.environment import Environment
from src.llm import get_llm_instance
from src.memory.information import Information
from src.memory.information_cache import InformationCache
from src.memory.long_term_memory import LongTermMemory
from src.task import get_stringified_all_available_task_name_description_pairs, \
    get_task_spec_path_by_name
from src.task.task_spec import TaskSpec
from src.utils.collection_utils import stringify_collection_as_unordered_list
from src.utils.environment_utils import get_agent_output_information_name
from src.utils.typed_dicts.interaction_history import InteractionHistory

load_dotenv()

AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE = 'current_objective'
AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES = 'information_queue_names'
AGENT_SPECIFIC_INFO_CACHE_KEYS = 'information_cache_keys'
USER_INPUT_INFO_QUEUE_NAME = 'user_input'
ALL_POSSIBLE_TASKS = 'all_possible_tasks'
EXECUTED_TASKS = 'executed_tasks'
RELEVANT_INFORMATION = 'relevant_information'
PAST_INFORMATION = 'past_information'

SPECIAL_INFORMATION_NAME_KEYS = [
    AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE,
    AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES,
    AGENT_SPECIFIC_INFO_CACHE_KEYS,
    ALL_POSSIBLE_TASKS,
    EXECUTED_TASKS,
    RELEVANT_INFORMATION,
    PAST_INFORMATION,
]

MAX_DEPTH = 3
RESPONSE_INFO_KEY = 'response'


class Agent:
    _agent_id: str
    _role_description: str
    _action_description_pairs: Dict[str,
                                    Tuple[Optional[str], Callable[..., Any]]]
    _task_specs_root_path: str
    _prompts_root_path: str
    _resource_root_path: str
    _task_specs: List[TaskSpec]
    _llm_instance: BaseChatModel
    _is_verbose: bool = False

    _current_objective: List[str]
    _task_history: List[str]
    _information_cache: InformationCache
    _long_term_memory: LongTermMemory
    _interaction_history: List[InteractionHistory]
    _is_process_finished: bool

    _environment: Optional[Environment]
    _in_information_queues: Dict[str, Optional[asyncio.Queue]]
    _out_information_queues: Dict[str, Optional[asyncio.Queue]]
    _agent_data_file_path: str

    _monitor_task: Optional[asyncio.Task]
    _stop_event: Optional[asyncio.Event]
    _pause_event: Optional[asyncio.Event]

    def __init__(
        self,
        agent_id: str,
        role_description: str,
        resource_root_path: str,
        information_cache: InformationCache,
        long_term_memory: LongTermMemory,
        environment: Optional[Environment] = None,
        in_information_queue_names: Optional[List[str]] = None,
        out_information_queue_names: Optional[List[str]] = None,
        llm_provider: str = 'openai',
        current_objective: Optional[str] = None,
        is_verbose: bool = False,
    ):
        self._agent_id = agent_id
        self._role_description = role_description
        self._resource_root_path = resource_root_path
        self._task_specs_root_path = os.path.join(
            resource_root_path, 'task_specs')
        self._prompts_root_path = os.path.join(resource_root_path, 'prompts')
        self._llm_instance = get_llm_instance(llm_provider)

        self._in_information_queues = dict()
        self._out_information_queues = dict()

        if current_objective is not None:
            self._current_objective = [current_objective]
        else:
            self._current_objective = []

        self._is_verbose = is_verbose
        self._task_history = []

        self.register_environment(environment)
        if in_information_queue_names is not None:
            for information_queue_name in in_information_queue_names:
                self.register_information_queue(information_queue_name, True)
        if out_information_queue_names is not None:
            for information_queue_name in out_information_queue_names:
                self.register_information_queue(information_queue_name, False)

        self._in_information_queues[USER_INPUT_INFO_QUEUE_NAME] = asyncio.Queue(
        )

        self._information_cache = information_cache
        self._long_term_memory = long_term_memory
        self._is_process_finished = False

        self._stop_event = None
        self._pause_event = None
        self._monitor_task = None

    async def listen(self, input_message: str):
        user_input_queue = self._in_information_queues.get(
            USER_INPUT_INFO_QUEUE_NAME)
        if user_input_queue is not None:
            await user_input_queue.put(Information(input_message, name=USER_INPUT_INFO_QUEUE_NAME))
            if self._is_verbose:
                print("Current", user_input_queue)
                print(self._in_information_queues[USER_INPUT_INFO_QUEUE_NAME])

    def see(self, environment_image_path: str):
        raise NotImplementedError

    def register_environment(self, environment: Optional[Environment]):
        if environment is not None:
            if self._environment is None:
                self._environment = environment
                self._environment.register_agent(self._agent_id)
                self.register_information_queue(
                    get_agent_output_information_name(self._agent_id), False)
        else:
            self._environment = None

    def register_information_queue(self, information_queue_name: str, is_incoming: bool = True):
        if is_incoming:
            if self._environment is not None:
                self._in_information_queues[information_queue_name] = \
                    self._environment.get_information_source_by_name(
                        information_queue_name)
            else:
                self._in_information_queues[information_queue_name] = None
        else:
            if self._environment is not None:
                self._out_information_queues[information_queue_name] = \
                    self._environment.get_information_source_by_name(
                        information_queue_name)
            else:
                self._out_information_queues[information_queue_name] = None

    def get_agent_id(self):
        return self._agent_id

    async def _monitor(self):
        if self._stop_event is None or self._pause_event is None:
            return
        
        while not self._stop_event.is_set():
            await self._pause_event.wait()
            for information_name in list(self._in_information_queues.keys()):
                queue = self._in_information_queues.get(information_name)
                if queue is not None and not queue.empty():
                    information = await queue.get()
                    if self._is_verbose:
                        print(
                            f'New information found in {information_name}: {information.value}')
                    self._information_cache.add_information(information)
                    await self._process(information)
                    queue.task_done()
            await asyncio.sleep(0.05)

    async def _process(self, information: Information, depth: int = 0):
        if depth >= MAX_DEPTH:
            if self._is_verbose:
                print(
                    'Hmm. There seems to be something wrong with your request. Please try again.')
            self._is_process_finished = True
            return
        if self._is_verbose:
            print(
                f'Processing information: {information.value} at depth {depth}')

        self._pause_monitor_task()

        task_spec_for_picked_task = await self._pick_a_task()
        if self._is_verbose:
            print("task_spec_for_picked_task returns",
                  task_spec_for_picked_task)

        if task_spec_for_picked_task is None:
            await self._process(information, depth + 1)
            return

        task_output = await self._execute_a_task(task_spec_for_picked_task)
        if self._is_verbose:
            print(
                f'task_output from processing at depth {depth}: {task_output}')

        if self._is_process_finished:
            self._reset()
            self._resume_monitor_task()
            return
        else:
            await self._process(information, depth + 1)

    async def _pick_a_task(self) -> Optional[TaskSpec]:
        task_spec = TaskSpec(
            self._task_specs_root_path,
            self._prompts_root_path,
            task_spec_path=os.getenv('TASK_SPEC_FOR_PICK_A_TASK')
        )
        result = await self._execute_a_task(task_spec)
        if 'task_pick_a_task_output:task_name' not in result or 'task_pick_a_task_output:reasoning' not in result:
            return None
        task_name = result['task_pick_a_task_output:task_name'].value
        reasoning = result['task_pick_a_task_output:reasoning'].value
        if self._is_verbose:
            print(f'Task picked: {task_name}')
            print(f'Reasoning: {reasoning}')
        return TaskSpec(
            self._task_specs_root_path,
            self._prompts_root_path,
            task_spec_path=get_task_spec_path_by_name(task_name)
        )

    async def _execute_a_task(self, task_spec: TaskSpec) -> Dict:
        task_name = task_spec.name
        if self._is_verbose:
            print(f'Executing task: {task_name}')

        arg_key_to_arg_val = self._build_arg_key_to_arg_val(task_spec)

        # Wrap synchronous actions inside to_thread to prevent blocking event loop
        action_output = await asyncio.to_thread(self._execute_actions, task_spec.action_names, arg_key_to_arg_val, self._is_verbose)

        informations = {}
        prompt_key_to_val = self._build_prompt_key_to_val(task_spec)

        if action_output is not None and len(task_spec.action_names) > 0:
            prompt_key_to_val['action_output'] = str(action_output)
            for key, val in action_output.items():
                prompt_key_to_val[key] = val
                key_with_task_name = f'task_{task_spec.name}_output:{key}'
                informations[key_with_task_name] = Information(
                    raw_value=val,
                    name=key_with_task_name
                )

        if task_spec.is_llm_task:
            task_instance = task_spec.build_task_instance(prompt_key_to_val)
            # Await the LLM generation heavily blocking mechanism gracefully
            triggered_info = await asyncio.to_thread(task_instance.trigger, self._llm_instance)
            informations.update(triggered_info)

        if self._is_verbose:
            print(f'Saving the following information to cache...')
        for information_name, information in informations.items():
            if self._is_verbose:
                print(f'{information}')
            self._information_cache.add_information(information)

        if task_spec.next_task is not None:
            next_task_output = await self._execute_a_task(task_spec.next_task)
            informations.update(next_task_output)

        if task_spec.is_response_generating_task:
            response_val = self._information_cache.get_most_recent_information_by_substring(
                RESPONSE_INFO_KEY).value
            await self._talk(str(response_val))

        self._is_process_finished = task_spec.is_terminating_task or self._is_process_finished
        if self._is_verbose:
            print(f'Is process finished? {self._is_process_finished}')

        self._task_history.append(task_spec.name)
        return informations

    @staticmethod
    def _execute_actions(action_names: List[str], arg_key_to_arg_val: Dict, is_verbose: bool) -> Optional[Dict]:
        if len(action_names) == 0:
            return None
        if is_verbose:
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

    def _record_interaction(self, content: str, is_input_message):
        raise NotImplementedError

    def _write(self):
        raise NotImplementedError

    def _read(self):
        raise NotImplementedError

    async def _talk(self, out_message: str):
        queue_name = get_agent_output_information_name(self._agent_id)
        if queue_name in self._out_information_queues:
            out_information_queue = self._out_information_queues[queue_name]
            if out_information_queue is not None:
                await out_information_queue.put(Information(out_message))
            else:
                if self._is_verbose:
                    print('No output information queue is set up.')
        else:
            if self._is_verbose:
                print('No output information queue is set up.')

    def _reset(self):
        self._current_objective = []
        self._task_history = []
        self._long_term_memory.add_short_term_memory(self._information_cache)
        self._information_cache.reset()
        self._is_process_finished = False

    def _load_action_description_pairs(self):
        self._action_description_pairs = get_all_available_action_data()

    def _get_special_information_key_to_val(self, task_spec: TaskSpec) -> Dict[str, str]:
        return {
            AGENT_SPECIFIC_INFO_CURRENT_OBJECTIVE: self._current_objective[0] if len(self._current_objective) > 0 else 'None',
            AGENT_SPECIFIC_INFO_CACHE_KEYS: self._information_cache.get_information_names_str(),
            AGENT_SPECIFIC_INFO_INFORMATION_QUEUE_NAMES: stringify_collection_as_unordered_list(list(self._in_information_queues.keys())),
            ALL_POSSIBLE_TASKS: get_stringified_all_available_task_name_description_pairs(),
            EXECUTED_TASKS: stringify_collection_as_unordered_list(self._task_history),
            RELEVANT_INFORMATION: self._information_cache.retrieve_stringified_information(
                self._current_objective[0] if len(
                    self._current_objective) > 0 else 'None', task_spec,
            ),
            PAST_INFORMATION: self._long_term_memory.retrieve_all_information_as_text(),
        }

    def _build_arg_key_to_arg_val(self, task_spec: TaskSpec) -> Dict[str, Any]:
        input_information_names = task_spec.input_information_names
        special_information_key_to_val = self._get_special_information_key_to_val(
            task_spec)
        arg_key_to_arg_val: Dict[str, Any] = {}
        for information_name in input_information_names:
            if information_name in SPECIAL_INFORMATION_NAME_KEYS:
                arg_key_to_arg_val[information_name] = special_information_key_to_val[information_name]
            elif self._information_cache.get_most_recent_information_name_containing_substring(information_name) is not None:
                information = self._information_cache.get_most_recent_information_by_substring(
                    information_name)
                arg_key_to_arg_val[information.name] = information.value
        arg_key_to_arg_val['information_cache'] = self._information_cache
        return arg_key_to_arg_val

    def _build_prompt_key_to_val(self, task_spec: TaskSpec) -> Dict[str, str]:
        prompt_key_to_val = self._get_special_information_key_to_val(task_spec)
        informations = self._information_cache.get_informations()
        for key in informations.keys():
            prompt_key_to_val[key] = (
                ' '.join([information.raw_value for information in informations[key]]))
        return prompt_key_to_val

    def start(self):
        if self._monitor_task is None or self._monitor_task.done():
            self._stop_event = asyncio.Event()
            self._pause_event = asyncio.Event()
            self._pause_event.set()
            self._monitor_task = asyncio.create_task(self._monitor())

    async def stop(self):
        if self._stop_event:
            self._stop_event.set()
            if self._pause_event:
                self._pause_event.set()
        if self._monitor_task:
            await self._monitor_task
            self._monitor_task = None

    def _pause_monitor_task(self):
        if self._pause_event:
            self._pause_event.clear()

    def _resume_monitor_task(self):
        if self._pause_event:
            self._pause_event.set()
