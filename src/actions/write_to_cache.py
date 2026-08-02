from pydantic import BaseModel, Field
from src.actions import action_tool
from src.core.memory.information_cache import InformationCache
from src.domain.models.memory.information import Information
from src.domain.enums.information_type import InformationType


class WriteToCacheArgs(BaseModel):
    key: str = Field(..., description="The exact name or key of the entity to remember (e.g., 'user_preferred_genre').")
    value: str = Field(...,
                       description="The detailed value, fact, or state to save.")


@action_tool(name="write_to_cache")
def write_to_cache(args: WriteToCacheArgs, information_cache: InformationCache, **kwargs) -> str:
    """Saves an extracted fact, user preference, or state entity into the active Core Memory (InformationCache)."""

    # Create the domain Information object
    info = Information(
        raw_value=args.value,
        name=args.key,
        # Defaulting to string for semantic facts
        information_type=InformationType.STRING
    )

    # Actively save it to the cache
    information_cache.add_information(info)

    return f"SYSTEM SUCCESS: Saved '{args.key}' with value '{args.value}' to Core Memory."
