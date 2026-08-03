import os
import json
from pathlib import Path
from typing import Tuple, List, Dict
from dotenv import load_dotenv

load_dotenv()

# --- Internal Cache to prevent repeated disk I/O ---
_TASK_CACHE_LOADED = False
_TASK_PATHS_CACHE: Dict[str, str] = {}
_TASK_DESCRIPTIONS_CACHE: Dict[str, str] = {}


def _ensure_tasks_loaded():
    """
    Dynamically scans the resources directory for JSON task specifications
    and builds the internal registry cache.
    """
    global _TASK_CACHE_LOADED, _TASK_PATHS_CACHE, _TASK_DESCRIPTIONS_CACHE
    if _TASK_CACHE_LOADED:
        return

    # Rely on the environment variable, just like TaskSpec does.
    # Fallback to a relative path if not defined.
    task_spec_root_str = os.getenv(
        'TASK_SPEC_DIR', 'resources/log_based_agent/task_specs/')

    # Resolve the absolute path of the root task specs directory
    base_dir = Path(os.getcwd())
    task_spec_dir = base_dir / task_spec_root_str

    # If not found via CWD, try relative to this file
    if not task_spec_dir.exists():
        task_spec_dir = Path(__file__).resolve(
        ).parent.parent.parent.parent / task_spec_root_str

    if not task_spec_dir.exists():
        print(
            f"WARNING: Could not locate Task Spec directory at {task_spec_dir}.")
        return

    # Recursively find all json files in the defined task_spec directory
    for json_path in task_spec_dir.rglob('*.json'):
        # Ignore template directories
        if '_template_' in json_path.parts:
            continue

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                spec_data = json.load(f)

            task_name = spec_data.get('name')
            description = spec_data.get(
                'description', 'No description provided.')

            if not task_name:
                continue

            # Version resolution: Prefer 'latest.json' if multiple exist
            existing_path = _TASK_PATHS_CACHE.get(task_name, "")
            if existing_path.endswith('latest.json') and json_path.name != 'latest.json':
                continue  # Keep the existing latest version

            try:
                rel_path = str(json_path.relative_to(task_spec_dir))
            except ValueError:
                # Fallback if relative_to fails
                rel_path = str(json_path.name)

            _TASK_PATHS_CACHE[task_name] = rel_path
            _TASK_DESCRIPTIONS_CACHE[task_name] = description

        except Exception as e:
            print(f"Error dynamically loading task spec {json_path}: {e}")

    _TASK_CACHE_LOADED = True


# --- Public Interface (Signatures Intact) ---

def get_task_spec_path_by_name(task_spec_name: str) -> str:
    _ensure_tasks_loaded()
    if task_spec_name not in _TASK_PATHS_CACHE:
        raise KeyError(
            f"Task '{task_spec_name}' not found. Ensure its JSON spec exists in {os.getenv('TASK_SPEC_DIR')}.")
    return _TASK_PATHS_CACHE[task_spec_name]


def get_all_task_spec_paths() -> Dict[str, str]:
    """
    Return a dynamically generated map of task names to their JSON file paths.
    """
    _ensure_tasks_loaded()
    return _TASK_PATHS_CACHE.copy()


def get_all_available_task_name_description_pairs() -> List[Tuple[str, str]]:
    """
    Dynamically fetch all defined tasks and return their name and description.
    """
    _ensure_tasks_loaded()
    return [(name, desc) for name, desc in _TASK_DESCRIPTIONS_CACHE.items()]


def get_stringified_all_available_task_name_description_pairs() -> str:
    """
    Returns a formatted string of all available tasks to be injected into LLM prompts.
    """
    pairs = get_all_available_task_name_description_pairs()
    s = ''
    for name, description in pairs:
        s += f'TASK_NAME: {name}\nTASK_DESCRIPTION: {description}\n***************\n'
    return s
