from typing import Dict, Literal, Union, Tuple, Any
from pydantic import BaseModel, ConfigDict, Field
from src.domain.enums.information_type import InformationType


class BaseInformationSpec(BaseModel):
    model_config = ConfigDict(strict=True)


class GenericInformationSpec(BaseInformationSpec):
    information_type: Literal[InformationType.BOOLEAN, InformationType.STRING]


class NumberInformationSpec(BaseInformationSpec):
    information_type: Literal[InformationType.INTEGER, InformationType.FLOAT]
    min_val: Union[int, float] = Field(default=float('-inf'))
    max_val: Union[int, float] = Field(default=float('inf'))


class ArrayInformationSpec(BaseInformationSpec):
    information_type: Literal[InformationType.ARRAY]
    item_type: InformationType


class TupleInformationSpec(BaseInformationSpec):
    information_type: Literal[InformationType.TUPLE]
    elements: Tuple[InformationType, ...]


class ObjectInformationSpec(BaseInformationSpec):
    information_type: Literal[InformationType.OBJECT]
    properties: Dict[str, 'InformationSpec']


InformationSpec = Union[
    GenericInformationSpec,
    NumberInformationSpec,
    ArrayInformationSpec,
    TupleInformationSpec,
    ObjectInformationSpec
]

ObjectInformationSpec.model_rebuild()


def parse_information_spec(information_spec_dict: dict) -> InformationSpec:
    """
    Parses a task spec dictionary into a strictly validated Pydantic model,
    safely handling raw strings and missing types to satisfy static type checkers like Pylance.
    """
    info_type_raw = information_spec_dict.get('information_type')
    if not isinstance(info_type_raw, str):
        raise TypeError(
            f"Expected string for 'information_type', got {type(info_type_raw)}")

    information_type = InformationType.__members__[info_type_raw.upper()]

    match information_type:
        case InformationType.STRING | InformationType.BOOLEAN:
            return GenericInformationSpec(information_type=information_type)

        case InformationType.INTEGER | InformationType.FLOAT:
            min_val = information_spec_dict.get('min_val')
            max_val = information_spec_dict.get('max_val')
            return NumberInformationSpec(
                information_type=information_type,
                min_val=min_val if min_val is not None else -float('inf'),
                max_val=max_val if max_val is not None else float('inf')
            )

        case InformationType.ARRAY:
            item_type_raw = information_spec_dict.get('item_type')
            if isinstance(item_type_raw, str):
                item_type = InformationType.__members__[item_type_raw.upper()]
            elif isinstance(item_type_raw, InformationType):
                item_type = item_type_raw
            else:
                raise ValueError(
                    f"Invalid or missing 'item_type' for ARRAY spec: {item_type_raw}")
            return ArrayInformationSpec(
                information_type=information_type,
                item_type=item_type
            )

        case InformationType.TUPLE:
            elements_raw = information_spec_dict.get('elements', [])
            elements = tuple(
                InformationType.__members__[
                    e.upper()] if isinstance(e, str) else e
                for e in (elements_raw or [])
            )
            return TupleInformationSpec(
                information_type=information_type,
                elements=elements
            )

        case InformationType.OBJECT:
            raw_props = information_spec_dict.get('properties', {})
            parsed_props = {
                k: parse_information_spec(v) if isinstance(v, dict) else v
                for k, v in (raw_props or {}).items()
            }
            return ObjectInformationSpec(
                information_type=information_type,
                properties=parsed_props
            )

        case _:
            raise TypeError(f"Unsupported InformationType: {information_type}")
