from typing import Dict
from pydantic import BaseModel, ConfigDict, StrictBool, StrictFloat


class ReviewResult(BaseModel):
    """Strictly validated ReviewResult replacing the old TypedDict."""
    model_config = ConfigDict(strict=True)

    is_acceptable: StrictBool
    criteria2scoring: Dict[str, float]
    overall_score: StrictFloat
