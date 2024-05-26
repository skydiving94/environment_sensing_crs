from enum import Enum


class InformationRelationType(Enum):
    """
    This is a collection of base relations.
    An agent should in the future be enabled to come up with a relation by itself and have it
    stored in a local storage.
    """
    IS_RELATED_TO = 'is_related_to'
    IS_A = 'is_a'
    CONTAINS = 'contains'
    CONTAINED_IN = 'contained_in'
    DERIVES = 'derives'
    DERIVED_FROM = 'derived_from'


class InformationRelation:
    information_relation_type: InformationRelationType | str

    def __init__(self, information_relation_type: str):
        try:
            self.information_relation_type = InformationRelationType(information_relation_type)
        except ValueError:
            self.information_relation_type = self.information_relation_type
