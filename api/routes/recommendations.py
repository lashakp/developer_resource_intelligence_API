from typing import Optional
from fastapi import APIRouter, Query

from api.schemas import RecommendationResponse
from api.service import get_recommendations as service_get_recommendations

router = APIRouter(prefix="/v1")


@router.get(
    "/recommendations",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="Get recommended developer resources",
    description="""
Return ranked developer resources for a given skill cluster.

⚠️ Note:
Some filter combinations may return zero results.
Use `/v1/debug/availability` to see valid skill → resource_type mappings.

Ranking:
- ML-based ranking is used if a trained model is available
- Falls back to deterministic scoring otherwise
""",
)
def get_recommendations(
    skill: str = Query(..., description="Skill cluster to search"),
    limit: int = Query(5, ge=1, le=100, description="Maximum number of results to return (pagination)"),
    offset: int = Query(0, ge=0, description="Number of results to skip (pagination)"),
    resource_type: Optional[str] = Query(None, description="Optional filter to only include resources of this type"),
    minimum_domain_weight: Optional[int] = Query(None, ge=0, description="Optional minimum domain weight to filter resources"),
):
    return service_get_recommendations(
        skill,
        limit=limit,
        offset=offset,
        resource_type=resource_type,
        minimum_domain_weight=minimum_domain_weight,
    )
