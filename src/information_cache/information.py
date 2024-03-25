from typing import Any, List, Tuple, Set, Dict, Optional

from src.information_cache.information_relation import InformationRelation
from src.utils.enums.information_type import InformationType
from src.utils.typed_dicts.information_spec import InformationSpec

Information_valueType = str | bool | int | float | List | Tuple | object


class Information:
    """
    Individual information.
    Can be thought of as a node in a graph/network of information, i.e. InformationCache.
    """

    # The raw _value of the information encoded as a string.
    _raw_value: str
    # The _value of the information parsed into its proper type.
    _value: Information_valueType
    # The _name of the information.
    _name: str
    # The type of this information.
    _information_type: InformationType
    # The info spec for this information.
    _information_spec: Optional[InformationSpec]
    # TODO: The neighbours of this information.
    _neighbors: Dict[InformationRelation, Set['Information']]
    # Whether the _value is correctly parsed.
    _is_value_parsed: bool

    def __init__(self,
                 raw_value: Any,
                 name: str = '',
                 information_type: InformationType = InformationType.STRING,
                 information_spec: Optional[InformationSpec] = None):
        self._raw_value = str(raw_value)
        self._name = name
        self._information_type = information_type
        self._is_value_parsed = True
        self._value = self._parse_raw_value_by_information_type(
            raw_value,
            information_type,
            information_spec)
        self._neighbors = dict()
        
    @property
    def raw_value(self):
        return self._raw_value

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @property
    def information_type(self):
        return self._information_type

    @property
    def information_spec(self):
        return self._information_spec

    @property
    def is_value_parse(self):
        return self._is_value_parsed

    def add_neighbor(
            self,
            information: 'Information',
            information_relation: InformationRelation):
        if information_relation not in self._neighbors:
            self._neighbors[information_relation] = set()
        self._neighbors[information_relation].add(information)

    def __str__(self):
        return f'Information Name: {self._name}; Information Value: {self._value}'

    def _parse_raw_value_by_information_type(
            self,
            _raw_value: Any,
            _information_type: InformationType,
            _information_spec: Optional[InformationSpec]) -> Information_valueType:
        """
        Given a raw _value and its type, parse it to its appropriate type.
        """

        _raw_value = str(_raw_value)
        match _information_type:
            case InformationType.STRING:
                return _raw_value
            case InformationType.BOOLEAN:
                return self._parse_bool(_raw_value)
            case InformationType.INTEGER:
                return int(_raw_value)
            case InformationType.FLOAT:
                return float(_raw_value)
            case InformationType.ARRAY:
                return self._parse_array(_raw_value, _information_spec)
            case InformationType.TUPLE:
                return self._parse_tuple(_raw_value, _information_spec)
            case InformationType.OBJECT:
                return self._parse_object(_raw_value, _information_spec)
            case _:
                raise TypeError

    def _parse_bool(self, _raw_value: str) -> str | bool:
        _raw_value = _raw_value.lower()
        if _raw_value in ['true', 'yes', '1']:
            return True
        elif _raw_value in ['false', 'no', '0']:
            return False
        else:
            self._is_value_parsed = False
            return _raw_value

    def _parse_array(
            self,
            _raw_value: str,
            _information_spec: Optional[InformationSpec]) -> List | str:
        if _information_spec is None:
            self._is_value_parsed = False
            return _raw_value

        # TODO: Postpone until actually needed.
        raise NotImplementedError

    def _parse_tuple(self, _raw_value: str, _information_spec: Optional[InformationSpec]) -> List:
        # TODO: Postpone until actually needed.
        raise NotImplementedError

    def _parse_object(self, _raw_value: str, _information_spec: Optional[InformationSpec]) -> List:
        # TODO: Postpone until actually needed.
        raise NotImplementedError
