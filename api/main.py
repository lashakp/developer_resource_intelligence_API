from fastapi import FastAPI

from api.schemas import (
    SkillListResponse,
    ResourceTypeListResponse,
    DomainListResponse,
    StatsResponse,
)

from api.service import (
    get_available_skills,
    get_available_resource_types,
    get_available_domains,
    get_stats,
)

from api.routes import recommendations
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


tags_metadata = [
    {
        "name": "Health",
        "description": "Service health and status checks",
    },
    {
        "name": "Discovery",
        "description": "Explore available skills, resource types, resource types and skills filter combinations, domains, and dataset statistics",
    },
    {
        "name": "Recommendations",
        "description": "Ranked developer resource recommendations (ML or deterministic)",
    },
    {
        "name": "Help",
        "description": "API usage guidance and examples",
    },
]


app = FastAPI(
    title="Developer Resource Intelligence API",
    version="1.0.0",
    description="Deterministic + ML-powered recommendation system for developer learning resources",
    openapi_tags=tags_metadata,
)


# ===== Health =====

@app.get("/v1/health", tags=["Health"])
def health():
    return {"status": "ok"}


# ===== Discovery =====

@app.get("/v1/skills", response_model=SkillListResponse, tags=["Discovery"])
def skills():
    skills = get_available_skills()
    return {
        "total": len(skills),
        "skills": skills,
    }


@app.get("/v1/resource-types", tags=["Discovery"])
def resource_types():
    resource_types = get_available_resource_types()
    return {
        "total": len(resource_types),
        "resource_types": resource_types,
    }


@app.get("/v1/domains", response_model=DomainListResponse, tags=["Discovery"])
def domains():
    domains = get_available_domains()
    return {
        "total": len(domains),
        "domains": domains,
    }

@app.get(
    "/v1/debug/availability",
    tags=["Discovery"],
    summary="Available filter combinations",
    description="Shows which resource types exist for each skill cluster"
)
def availability():
    from api.service import get_filter_availability
    return get_filter_availability()


@app.get(
    "/v1/stats",
    response_model=StatsResponse,
    tags=["Discovery"],
    summary="Dataset statistics",
    description="High-level statistics about skills and domains in the dataset",
)
def stats():
    return get_stats()


# ===== Help =====

@app.get(
    "/v1/help",
    tags=["Help"],
    summary="API usage guide",
    description="Human-readable guide for using the Developer Resource Intelligence API",
)
def help():
    return {
        "overview": "This API provides ranked recommendations for developer learning resources.",
        "key_concepts": {
            "skill_cluster": "Broad developer domains such as backend, frontend, data, devops, mobile.",
            "resource_type": "Type of resource such as tool, documentation, course, or article.",
            "domain_weight": (
                "A heuristic authority score. Higher values indicate more established or trusted domains."
            ),
            "ranking": {
                "ml": "ML-based ranking if a trained model is available",
                "fallback": "Deterministic scoring otherwise",
            },
            "pagination": {
                "limit": "Number of results returned per request",
                "offset": "How many results to skip before returning data",
            },
        },
        "example_requests": {
            "basic": "/v1/recommendations?skill=backend",
            "filtered": "/v1/recommendations?skill=data&resource_type=tool&min_domain_weight=3",
            "paginated": "/v1/recommendations?skill=frontend&limit=5&offset=5",
        },
    }


# ===== Routers =====

app.include_router(recommendations.router)
