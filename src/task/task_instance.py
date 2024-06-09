import json
from typing import Dict

from langchain_core.language_models import BaseChatModel

from src.memory.information import Information
from src.utils.enums.information_type import InformationType
from src.utils.typed_dicts.information_spec import InformationSpec, GenericInformationSpec


class TaskInstance:
    # Name of the task
    name: str

    # System prompt to LLM
    system_prompt: str

    # Task specific prompt to LLM
    task_prompt: str

    # The temperature when llm is invoked for this instance.
    temperature: float

    # Output information type for this task.
    output_information_spec: Dict[str, InformationSpec]

    def __init__(self,
                 name: str,
                 system_prompt: str,
                 task_prompt: str,
                 temperature: float,
                 output_information_spec: Dict[str, InformationSpec]):
        self.name = name
        self.system_prompt = system_prompt
        self.task_prompt = task_prompt
        self.temperature = temperature
        self.output_information_spec = output_information_spec

    def trigger(self, llm_instance: BaseChatModel) -> Dict[str, Information]:
        max_retry = 5
        count = 0
        error_message_added = False
        response_data = {}
        while count < max_retry:
            count += 1
            response = llm_instance.invoke(
                self.task_prompt,
                temperature=self.temperature,
                max_tokens=500,
                top_p=1.0,
                timeout=10)
            try:
                response_data = json.loads(str(response.content))
                break
            except Exception as e:
                print("Parsing Json Error", response.content, "Exception:", e)
                if not error_message_added:
                    self.task_prompt += (
                        '\nERROR: The previous output is not parsable!!!! '
                        'Make sure the output string can be properly parsed!!!'
                        f'please correct it according following message: {e}')
                    error_message_added = True
            
        informations = dict()
        for key in response_data.keys():
            if key not in self.output_information_spec.keys() and key != 'json_output':
                return {}
            if key == 'json_output':
                info_spec = GenericInformationSpec(information_type=InformationType.STRING)
            else:
                info_spec = self.output_information_spec[key]
            raw_value = response_data[key]

            # Append the task name to the front of the action output.
            key_with_task_name = f'task_{self.name}_output:{key}'
            informations[key_with_task_name] = Information(
                raw_value,
                key_with_task_name,
                info_spec['information_type'],
                info_spec)
        return informations
