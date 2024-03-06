from typing import Dict, TypedDict, Literal, Union, Tuple

from src.utils.enums.information_type import InformationType


# FIXME: The following code can be problematic due to wrongly used TypedDict and Enum as types.
#   Hence it may be subjected to change in the future.


class GenericInformationSpec(TypedDict):
    information_type: Literal[InformationType.BOOLEAN] | Literal[InformationType.STRING]


class NumberInformationSpec(TypedDict):
    information_type: Literal[InformationType.INTEGER] | Literal[InformationType.FLOAT]
    min_val: int | float
    max_val: int | float


class ArrayInformationSpec(TypedDict):
    information_type: Literal[InformationType.ARRAY]
    item_type: InformationType


class TupleInformationSpec(TypedDict):
    information_type: Literal[InformationType.TUPLE]
    elements: Tuple[InformationType, ...]


class ObjectInformationSpec(TypedDict):
    information_type: Literal[InformationType.OBJECT]
    properties: Dict[str, 'InformationSpec']  # Using the forward-declare feature in Python.


InformationSpec = Union[
    GenericInformationSpec,
    NumberInformationSpec,
    ArrayInformationSpec,
    TupleInformationSpec,
    ObjectInformationSpec
]


def parse_information_spec(information_spec_dict: dict) -> InformationSpec:
    information_type = InformationType.__members__[
        information_spec_dict['information_type'].upper()]

    match information_type:
        case InformationType.STRING | InformationType.BOOLEAN:
            return GenericInformationSpec(information_type=information_type)
        case InformationType.INTEGER | InformationType.FLOAT:
            min_val = information_spec_dict['min_val']
            max_val = information_spec_dict['max_val']
            return NumberInformationSpec(information_type=information_type,
                                         min_val=min_val if min_val is not None else -float('inf'),
                                         max_val=max_val if max_val is not None else float('inf'))
        case InformationType.ARRAY:
            return ArrayInformationSpec(information_type=information_type,
                                        item_type=information_spec_dict['item_type'])
        case InformationType.TUPLE:
            return TupleInformationSpec(information_type=information_type,
                                        elements=information_spec_dict['elements'])
        case InformationType.OBJECT:
            return ObjectInformationSpec(information_type=information_type,
                                         properties=information_spec_dict['properties'])
        case _:
            raise TypeError
