from typing import List


class TaskInstance:
    # Name of the task
    name: str

    # System prompt to LLM
    system_prompt: str

    # Task specific prompt to LLM
    task_prompt: str

    # The action pipeline.
    action_names: List[str]

    def __init__(self,
                 name: str,
                 system_prompt: str,
                 task_prompt: str,
                 action_names: List[str]):
        self.name = name
        self.system_prompt = system_prompt
        self.task_prompt = task_prompt
        self.action_names = action_names
