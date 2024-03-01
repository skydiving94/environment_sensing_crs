import json
from typing import Dict, List

from dotenv import load_dotenv

from src.task.task_instance import TaskInstance
from src.typed_dicts.information_spec import InformationSpec, parse_information_spec
from src.utils.prompt_utils import load_prompt_template, replace_all_keys_in_prompt_template

load_dotenv()

PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT = load_prompt_template('PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT_PATH')


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
    output_information_spec: InformationSpec
    output_information_spec_str: str

    # The action pipeline.
    action_names: List[str]

    def __init__(self, task_spec_str: str):
        task_spec_dict = json.loads(task_spec_str)
        self.name = task_spec_dict['name']
        self.description = task_spec_dict['description']

        self.system_prompt_template = load_prompt_template(task_spec_dict['system_prompt_template'])
        self.task_prompt_template = load_prompt_template(task_spec_dict['task_prompt_template'])

        self.input_information_names = task_spec_dict['input_information_names']
        self.output_information_spec = parse_information_spec(
            task_spec_dict['output_information_spec'])
        self.output_information_spec_str = json.dumps(task_spec_dict['output_information_spec'])

    def build_task_instance(self,
                            system_prompt_key_to_val: Dict[str, str],
                            task_prompt_key_to_val: Dict[str, str]) -> TaskInstance:
        system_prompt = replace_all_keys_in_prompt_template(self.system_prompt_template,
                                                            system_prompt_key_to_val)
        task_prompt = \
            (replace_all_keys_in_prompt_template(self.task_prompt_template,
                                                 task_prompt_key_to_val)
             + replace_all_keys_in_prompt_template(PROMPT_TEMPLATE_FOR_TASK_SPEC_OUTPUT,
                                                   {'output_format': self.output_information_spec_str}))
        return TaskInstance(name=self.name,
                            system_prompt=system_prompt,
                            task_prompt=task_prompt,
                            action_names=self.action_names)
