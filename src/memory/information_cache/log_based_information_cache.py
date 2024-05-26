from abc import ABC

from src.memory.information_cache import InformationCache


class LogBasedInformationCache(InformationCache, ABC):
    def __init__(self):
        super().__init__()
