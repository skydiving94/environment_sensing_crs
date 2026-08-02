from typing import Dict
from src.service.llm.base_client import BaseLLMClient
from src.adapters.prompt_builder.base_schema_builder import BaseSchemaBuilder
from src.adapters.response_parser.base_response_parser import BaseResponseParser
from src.domain.models.memory.information import Information
from src.domain.models.task_spec.information_spec import InformationSpec


class TaskInstance:
    def __init__(self, name: str, system_prompt: str, task_prompt: str, temperature: float, output_information_spec: Dict[str, InformationSpec]):
        self.name = name
        self.system_prompt = system_prompt
        self.task_prompt = task_prompt
        self.temperature = temperature
        self.output_information_spec = output_information_spec

    async def trigger(
        self,
        llm_instance: BaseLLMClient,
        schema_builder: BaseSchemaBuilder,
        response_parser: BaseResponseParser
    ) -> Dict[str, Information]:

        # 1. Translate Domain to Provider
        output_tool = schema_builder.build_task_output_tool(
            self.name, self.output_information_spec)
        tool_choice = {"type": "function", "function": {
            "name": output_tool["function"]["name"]}}

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.task_prompt}
        ]

        # 2. Pure I/O execution
        response = await llm_instance.generate_response(
            messages=messages,
            tools=[output_tool],
            tool_choice=tool_choice
        )

        # 3. Translate Provider to Domain
        response_data = response_parser.extract_json_from_tool_call(response)

        # 4. Domain processing
        informations = dict()
        for key in response_data.keys():
            if key not in self.output_information_spec.keys():
                continue
            info_spec = self.output_information_spec[key]
            raw_value = response_data[key]
            key_with_task_name = f'task_{self.name}_output:{key}'
            informations[key_with_task_name] = Information(
                raw_value, key_with_task_name, info_spec.information_type, info_spec)

        return informations
