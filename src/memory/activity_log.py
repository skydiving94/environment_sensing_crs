from datetime import datetime

from src.utils.enums.activity_log_type import ActivityLogType


class ActivityLog:
    """
    A single entry that contains information given by users, output by the agent,
    or internal, intermediary thought process by the agent.
    """
    log_type: ActivityLogType
    log_text: str
    log_time: datetime

    def __init__(self, log_type: ActivityLogType, log_text: str, log_time: datetime):
        self.log_type = log_type
        self.log_text = log_text
        self.log_time = log_time

    def __str__(self):
        return f'{self.log_type} @ {self.log_time}: {self.log_text}\n---------'

