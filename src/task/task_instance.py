import json
from typing import Dict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

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

    def run(self, llm_instance: BaseChatModel) -> Dict[str, Information]:
        system_message = SystemMessage(content=self.system_prompt)
        ai_message = AIMessage(content=self.task_prompt)
        message = [system_message, ai_message]
        response = llm_instance.invoke(
            message,
            temperature=0.0,
            max_tokens=120,
            top_p=1.0,
            timeout=10)
        response_data = json.loads(str(response.content))
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
