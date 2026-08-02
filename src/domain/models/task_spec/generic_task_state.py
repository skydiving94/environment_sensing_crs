from typing import Dict, Any
from pydantic import BaseModel, ConfigDict


class GenericTaskState(BaseModel):
    """
    Replaces CRS-specific TypedDicts (like InteractionHistory) with a generic, 
    strictly validated Pydantic model.
    """
    # extra='allow' permits dynamic key-value state injection for generic tasks
    # while strict=True validates any explicitly typed fields.
    model_config = ConfigDict(strict=True, extra='allow')

    # Core state variables can be strictly typed here:
    agent_id: str | None = None
