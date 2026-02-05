from typing import Optional

from fastapi import APIRouter, Query, Header

from api.schemas import RecommendationResponse
from api.service import get_recommendations as service_get_recommendations
from api.auth import verify_api_key_optional

router = APIRouter(prefix="/v1")


@router.get(
    "/recommendations",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="Get recommended developer resources",
    description="""
Return a ranked list of developer learning resources for a given skill cluster.

### Filters
You may optionally filter by resource type or minimum domain weight.

⚠️ **Note**
Some filter combinations may return zero results.
Use `/v1/debug/availability` to see valid skill → resource_type mappings.

Note: Skill values are case-insensitive (e.g. `data`, `Data`, and `DATA` are treated the same).

---

### Access Modes

🔓 **Demo mode** (no API key)
- Maximum of 5 results
- Deterministic (non-ML) ranking
- Intended for exploration and testing

🔐 **Full mode** (valid API key)
- Full result set
- ML-based ranking when a trained model is available

Provide your API key using the request header:

`X-API-Key: your-api-key`
""",
)
def get_recommendations(
    skill: str = Query(
        ...,
        description="Skill cluster to retrieve recommendations for (e.g. 'data', 'backend')",
    ),
    limit: int = Query(
        5,
        ge=1,
        le=100,
        description="Maximum number of results to return (pagination limit)",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of results to skip (pagination offset)",
    ),
    resource_type: Optional[str] = Query(
        None,
        description="Optional filter to include only a specific resource type (e.g. course, article)",
    ),
    minimum_domain_weight: Optional[int] = Query(
        None,
        ge=0,
        description="Optional minimum domain relevance score required for results",
    ),
    x_api_key: Optional[str] = Header(
        default=None,
        description="Optional API key. Required for full access mode",
    ),
):
    access_mode = verify_api_key_optional(x_api_key)

    return service_get_recommendations(
        skill=skill,
        limit=limit,
        offset=offset,
        resource_type=resource_type,
        minimum_domain_weight=minimum_domain_weight,
        access_mode=access_mode,
    )
