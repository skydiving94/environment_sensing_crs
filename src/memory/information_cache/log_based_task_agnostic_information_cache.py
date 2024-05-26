from src.memory.information_cache.log_based_information_cache import LogBasedInformationCache
from src.task.task_spec import TaskSpec


class LogBasedTaskAgnosticInformationCache(LogBasedInformationCache):
    def __init__(self):
        super().__init__()

    def retrieve_stringified_information(
        self,
        objective: str,
        task_spec: TaskSpec
    ):
        return f'Activity Logs:\n{self.get_activity_logs_str()}'

    def reset(self):
        self.initialize()

    def initialize(self):
        super().initialize()

    def __str__(self) -> str:
        return f'Activity Logs:\n{self.get_activity_logs_str()}'
