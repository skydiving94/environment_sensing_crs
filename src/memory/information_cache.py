from typing import Set, Dict, List

from src.memory.activity_log import ActivityLog
from src.memory.information import Information
from src.memory.information_relation import InformationRelation
from src.utils.collection_utils import stringify_collection_as_unordered_list


class InformationCache:
    """
    A graph/network of Information nodes and other InformationCache nodes.
    That is, an information cache can be a network, and also a node of a bigger information cache.
    FIXME: the details of the design is yet to be determined and is subject to change.
    """

    # A list of all activity logs stored for this information cache.
    activity_logs: List[ActivityLog]

    # A collection of all informations in a map of info name to a set of actual information.
    # TODO: replace Dict with a priority queue.
    # TODO: periodically cluster all unnamed information and assign each group a name.
    _informations: Dict[str, List[Information]]

    # Related information cache.
    _neighbors: Dict[InformationRelation, Set['InformationCache']]

    def __init__(self):
        self._informations = dict()
        self._neighbors = dict()

    def add_activity_log(self, activity_log: ActivityLog):
        self.activity_logs.append(activity_log)

    def add_information(self, information: Information):
        information_name = information.name
        if information_name not in self._informations:
            self._informations[information_name] = list()
        self._informations[information_name].append(information)

    def add_neighbor(
            self,
            information_cache: 'InformationCache',
            information_relation: InformationRelation):
        if information_relation not in self._neighbors:
            self._neighbors[information_relation] = set()
        self._neighbors[information_relation].add(information_cache)

    def get_activity_logs_str(self) -> str:
        return stringify_collection_as_unordered_list(self.activity_logs)

    def get_information_names_str(self) -> str:
        return stringify_collection_as_unordered_list(self.get_information_names())

    def get_information_names(self) -> List[str]:
        return list(self._informations.keys())

    def get_information_by_name(self, information_name: str) -> List[Information]:
        if information_name in self._informations:
            return self._informations[information_name]
        else:
            print("Accessing non-exist information: ", information_name)
            return []

    def get_top_information_by_name(self, information_name: str) -> Information:
        """
        It gets the information for the given name with the highest priority.
        """
        information_list = self.get_information_by_name(information_name)
        return information_list[-1]

    def get_informations(self) -> Dict[str, List[Information]]:
        return self._informations
