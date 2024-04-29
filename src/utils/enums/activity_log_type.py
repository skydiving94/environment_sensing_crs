from enum import Enum


class ActivityLogType(Enum):
    USER_INPUT = 'user_input'
    AGENT_OUTPUT = 'agent_output'
    INTERMEDIARY = 'intermediary'
