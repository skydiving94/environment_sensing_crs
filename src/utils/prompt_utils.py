import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


def load_prompt_template(prompt_template_path: str) -> str:
    if prompt_template_path is not None and os.path.exists(prompt_template_path):
        with open(prompt_template_path) as fp:
            return fp.read()
    else:
        return prompt_template_path


def replace_all_keys_in_prompt_template(prompt_template: str, key_to_val: Dict[str, str]) -> str:
    return prompt_template.format(**key_to_val)
