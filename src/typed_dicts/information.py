from typing import TypedDict


class Information(TypedDict):
    name: str
    raise NotImplementedError


def parse_information(information_str) -> Information:
    raise NotImplementedError
