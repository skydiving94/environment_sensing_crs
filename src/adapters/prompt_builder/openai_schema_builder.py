from typing import Dict, Any
from .base_schema_builder import BaseSchemaBuilder
from src.domain.models.task_spec.information_spec import InformationSpec
from src.domain.enums.information_type import InformationType


class OpenAISchemaBuilder(BaseSchemaBuilder):
    def _map_info_type_to_json_schema(self, info_type: InformationType) -> str:
        mapping = {
            InformationType.STRING: "string",
            InformationType.INTEGER: "integer",
            InformationType.FLOAT: "number",
            InformationType.BOOLEAN: "boolean",
            InformationType.ARRAY: "array",
            InformationType.OBJECT: "object",
            InformationType.TUPLE: "array"
        }
        return mapping.get(info_type, "string")

    def build_task_output_tool(self, task_name: str, output_spec: Dict[str, InformationSpec]) -> Dict[str, Any]:
        properties = {}
        required_keys = []

        for key, spec in output_spec.items():
            properties[key] = {
                "type": self._map_info_type_to_json_schema(spec.information_type)
            }
            required_keys.append(key)

        return {
            "type": "function",
            "function": {
                "name": f"submit_{task_name}_output".replace("-", "_"),
                "description": f"Submit the final structured data for the {task_name} task.",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_keys,
                    "additionalProperties": False
                }
            }
        }
