from typing import Iterable


def stringify_collection_as_unordered_list(items: Iterable) -> str:
    res = ''
    for item in items:
        res += f'- {str(item)}\n'
    return res
