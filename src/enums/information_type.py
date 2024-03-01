from enum import Enum


class InformationType(Enum):
    BOOLEAN = 'boolean'
    INTEGER = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    ARRAY = 'array'
    TUPLE = 'tuple'
    OBJECT = 'object'
