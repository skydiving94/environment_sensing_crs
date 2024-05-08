from typing import Optional, List


def find_latest_information_with_substring(
    information_names: List[str],
    information_name_substring: str
) -> Optional[str]:
    for information_name in reversed(information_names):
        if information_name.endswith(f':{information_name_substring}'):
            return information_name
    return None
