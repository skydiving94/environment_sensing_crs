import importlib
import inspect
import pkgutil
from typing import Callable, Any, Tuple, Optional, Dict

_ACTION_REGISTRY: Dict[str, Tuple[Optional[str], Callable[..., Any]]] = {}


def action_tool(name: str):
    """Decorator to regsiter an action tool in the central ActionRegistry."""
    def decorator(func: Callable[..., Any]):
        docstring = inspect.getdoc(func) or f"Execute {name} action."
        _ACTION_REGISTRY[name] = (docstring, func)
        return func
    return decorator


def _load_all_actions():
    """Dynamically imports all modules in the src.agent.actions package to trigger the 
    @action_tool decorators and populate the registry on startup."""
    import src.actions
    for _, module_name, is_pkg in pkgutil.iter_modules(src.actions.__path__):
        if not is_pkg:
            importlib.import_module(f"src.actions.{module_name}")


def get_all_available_action_data() -> Dict[str, Tuple[Optional[str], Callable[..., Any]]]:
    """Fetch all dynamically registered actions, together with their doc string descriptions.
    :return: A dict mapping the name of the action to its description and callable function.
    """
    if not _ACTION_REGISTRY:
        _load_all_actions()
    return _ACTION_REGISTRY
