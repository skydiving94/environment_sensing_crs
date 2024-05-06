from src.memory.information_cache import InformationCache
from src.task.task_spec import TaskSpec


class ChatBasedTaskAgnosticInformationCache(InformationCache):
    def __init__(self):
        super().__init__()

    def retrieve_stringified_information(
        self,
        objective: str,
        task_spec: TaskSpec
    ):
        return f'Historical Activity Logs:\n{self.get_activity_logs_str()}'
