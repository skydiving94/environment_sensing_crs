from typing import TypedDict


class TaskSpec(TypedDict):
    pass


def parse_task_spec(task_spec_text: str) -> TaskSpec:
    pass


def validate_task_spec(task_spec_text: str) -> str:
    pass


def load_task_spec(task_spec_path: str) -> str:
    pass
