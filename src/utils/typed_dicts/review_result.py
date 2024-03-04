from typing import TypedDict


class ReviewResult(TypedDict):
    is_acceptable: bool
    criteria2scoring: dict
    overall_score: float
