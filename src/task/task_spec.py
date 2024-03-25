import json
from typing import Dict, List, Optional

from dotenv import load_dotenv

from src.task.task_instance import TaskInstance
from src.utils.prompt_utils import load_prompt_template, replace_all_keys_in_prompt_template
from src.utils.typed_dicts.information_spec import InformationSpec, parse_information_spec

load_dotenv()

PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT = load_prompt_template(
    'PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT_PATH')


class TaskSpec:
    """
    The definition of type for s task spec, which is to be parsed from a definition in JSON.
    """

    # The name of the task
    name: str

    # A brief description of the task to be reviewed by humans/agents.
    description: str

    # System prompt to LLM
    system_prompt_template: str

    # Task specific prompt to LLM
    task_prompt_template: str

    # Names of the information needed for the task
    input_information_names: List[str]

    # Names and types of the information produced by the task
    output_information_spec: Dict[str, InformationSpec]
    output_information_spec_str: str

    # The action pipeline.
    action_names: List[str]

    # The temperature for when the task is executed.
    temperature: float

    # Whether the task is llm_task
    is_llm_task: bool

    # What is the next task of the current one, if any
    next_task: Optional['TaskSpec']

    def __init__(self, task_spec_str: Optional[str] = None, task_spec_path: Optional[str] = None):
        task_spec_dict: Dict = self._load_task_spec_dict(task_spec_path, task_spec_str)

        output_information_spec = task_spec_dict['output_information_spec']
        self.name = task_spec_dict['name']
        self.description = task_spec_dict['description']

        self.system_prompt_template = load_prompt_template(task_spec_dict['system_prompt_template'])
        self.task_prompt_template = load_prompt_template(task_spec_dict['task_prompt_template'])

        self.input_information_names = task_spec_dict['input_information_names']
        self.output_information_spec = \
            {k: parse_information_spec(v) for k, v in output_information_spec.items()}
        self.output_information_spec_str = json.dumps(output_information_spec)
        self.action_names = task_spec_dict['action_names']
        self.temperature = task_spec_dict['temperature'] \
            if 'temperature' in task_spec_dict \
            else 0.5
        self.is_terminating_task = task_spec_dict['is_terminating_task'] \
            if 'is_terminating_task' in task_spec_dict \
            else False
        self.is_llm_task = task_spec_dict['is_llm_task']
        self.next_task = TaskSpec(task_spec_str=task_spec_dict['next_task'])

    def build_task_instance(
            self,
            prompt_key_to_val: Dict[str, str]) -> TaskInstance:
        system_prompt = replace_all_keys_in_prompt_template(self.system_prompt_template,
                                                            prompt_key_to_val)
        task_prompt = \
            (replace_all_keys_in_prompt_template(self.task_prompt_template,
                                                 prompt_key_to_val)
             # make sure there is a newline between the task prompt and the output prompt
             + "\n"
             + replace_all_keys_in_prompt_template(
                        PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT,
                        {'output_format': self.output_information_spec_str}))
        return TaskInstance(name=self.name,
                            system_prompt=system_prompt,
                            task_prompt=task_prompt,
                            temperature=self.temperature,
                            output_information_spec=self.output_information_spec)

    @staticmethod
    def _load_task_spec_dict(task_spec_path, task_spec_str):
        if ((task_spec_str is None and task_spec_path is None)
                or (task_spec_str is not None and task_spec_path is not None)):
            raise ValueError('Exactly one of task_spec_str or task_spec_path should be provided.')
        elif task_spec_path is not None:
            with open(task_spec_path) as fp:
                task_spec_str = fp.read()
                task_spec_dict = json.loads(task_spec_str)
        elif task_spec_str is not None:
            task_spec_dict = json.loads(task_spec_str)
        else:
            raise ValueError
        return task_spec_dict
