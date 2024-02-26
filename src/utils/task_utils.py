from src.typed_dicts.task_spec import TaskSpec


def parse_task_spec(task_spec_text: str) -> TaskSpec:
    raise NotImplementedError


def validate_task_spec(task_spec_text: str) -> str:
    raise NotImplementedError


def load_task_spec(task_spec_path: str) -> str:
    raise NotImplementedError
