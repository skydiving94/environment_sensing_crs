from typing import Set, Dict, List

from src.information_cache.information import Information
from src.information_cache.information_relation import InformationRelation


class InformationCache:
    """
    A graph/network of Information nodes and other InformationCache nodes.
    That is, an information cache can be a network, and also a node of a bigger information cache.
    FIXME: the details of the design is yet to be determined and is subject to change.
    """

    # A collection of all informations in a map of info name to a set of actual information.
    # TODO: replace Dict with a priority queue.
    # TODO: periodically cluster all unnamed information and assign each group a name.
    _informations: Dict[str, List[Information]]

    # Related information cache.
    _neighbors: Dict[InformationRelation, Set['InformationCache']]

    def __init__(self):
        self._informations = dict()
        self._neighbors = dict()

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

    def get_information_names_str(self) -> str:
        return ' '.join(self.get_information_names())

    def get_information_names(self) -> List[str]:
        return list(self._informations.keys())

    def get_information_by_name(self, information_name: str) -> List[Information]:
        return self._informations[information_name]

    def get_top_information_by_name(self, information_name: str) -> List[Information]:
        """
        It gets the information for the given name with the highest priority.
        """
        raise NotImplementedError

    def get_informations(self) -> Dict[str, List[Information]]:
        return self._informations
