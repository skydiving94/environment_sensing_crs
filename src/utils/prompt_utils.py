import os
import re
from typing import Dict, Set

from dotenv import load_dotenv

load_dotenv()


def load_prompt_template(prompt_template: str) -> str:
    prompt_template_path = os.getenv(prompt_template)
    if prompt_template_path is not None and os.path.exists(prompt_template_path):
        with open(prompt_template_path) as fp:
            return fp.read()
    else:
        return prompt_template


def replace_all_keys_in_prompt_template(prompt_template: str, key_to_val: Dict[str, str]) -> str:
    for key in key_to_val.keys():
        prompt_template = prompt_template.replace(f'[[{key}]]', key_to_val[key])
    return prompt_template


def extract_replaceable_keys(prompt_template: str) -> Set[str]:
    pattern = r"\[\[(.*?)\]\]"
    matches = re.findall(pattern, prompt_template)
    return set(matches)
