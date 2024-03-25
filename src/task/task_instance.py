import json
from typing import Dict

from langchain_core.language_models import BaseChatModel

from src.information_cache.information import Information
from src.utils.typed_dicts.information_spec import InformationSpec


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
        # How do I get information here? 'Find the best top rating movie in 2021.'
        max_retry = 5
        count = 0
        error_message_added = False
        while count < max_retry:
            count += 1
            response = llm_instance.invoke(
                self.task_prompt,
                temperature=0.0,
                max_tokens=500,
                top_p=1.0,
                timeout=10)
            try:
                response_data = json.loads(str(response.content))
                break
            except Exception as e:
                print("Parsing Json Error", response.content, "Exception:", e)
                # Add error message to task_prompt
                self.task_prompt += "\nJson string is not parsable, please correct it according following message: " + str(e)
                error_message_added = True
            
        informations = dict()
        for key in response_data.keys():
            if key not in self.output_information_spec.keys():
                return {}
            info_spec = self.output_information_spec[key]
            raw_value = response_data[key]
            informations[key] = Information(
                raw_value,
                key,
                info_spec['information_type'],
                info_spec)
        return informations
