from pydantic import BaseModel
from typing import List, Optional


class Resource(BaseModel):
    resource_id: str
    resource_name: str
    source_url: str
    domain: str
    category: str
    resource_type: str
    skill_cluster: str
    domain_weight: int
    score: Optional[float] = None


class SkillListResponse(BaseModel):
    total: int
    skills: List[str]


class ResourceTypeListResponse(BaseModel):
    total: int
    resource_types: List[str]


class DomainItem(BaseModel):
    domain: str
    count: int


class DomainListResponse(BaseModel):
    total: int
    domains: List[DomainItem]
    
    
class SkillStatItem(BaseModel):
    skill_cluster: str
    count: int

class ResourceTypeStatItem(BaseModel):
    resource_type: str
    count: int


class StatsResponse(BaseModel):
    total_resources: int
    top_skills: List[SkillStatItem]
    top_domains: List[DomainItem]
    resource_types: List[ResourceTypeStatItem]    


class RecommendationResponse(BaseModel):
    skill_cluster: str
    count: int
    ranking_mode: Optional[str] = None
    # Backwards-compatible alias
    total_results: Optional[int] = None
    results: List[Resource]

    class Config:
        json_schema_extra = {
            "example": {
                "skill_cluster": "backend",
                "count": 1,
                "ranking_mode": "deterministic",
                "results": [
                    {
                        "resource_id": "abc123",
                        "resource_name": "FastAPI Documentation",
                        "source_url": "https://fastapi.tiangolo.com",
                        "domain": "fastapi.tiangolo.com",
                        "category": "framework",
                        "resource_type": "documentation",
                        "skill_cluster": "backend",
                        "domain_weight": 5,
                        "score": 8.5
                    }
                ]
            }
        }
