from typing import List, Dict
from collections import Counter

from api.data import RESOURCES
from api.service.ranking import rank_resource



# ===== Discovery =====

def get_available_skills() -> List[str]:
    return sorted({r["skill_cluster"] for r in RESOURCES})


def get_available_resource_types() -> List[str]:
    return sorted({r["resource_type"] for r in RESOURCES})


def get_filter_availability() -> Dict:
    availability = {}
    for r in RESOURCES:
        availability.setdefault(r["skill_cluster"], set()).add(r["resource_type"])
    return {k: sorted(v) for k, v in availability.items()}


def get_available_domains() -> List[Dict]:
    counter = Counter(r["domain"] for r in RESOURCES)
    return [{"domain": d, "count": c} for d, c in counter.most_common()]


def get_stats(top_n: int = 5) -> Dict:
    return {
        "total_resources": len(RESOURCES),
        "top_skills": Counter(r["skill_cluster"] for r in RESOURCES).most_common(top_n),
        "top_domains": Counter(r["domain"] for r in RESOURCES).most_common(top_n),
        "resource_types": Counter(r["resource_type"] for r in RESOURCES).most_common(),
    }


# ===== Recommendations =====

def get_recommendations(
    skill: str,
    limit: int = 5,
    offset: int = 0,
    resource_type: str | None = None,
    minimum_domain_weight: int | None = None,
):
    resources = [r.copy() for r in RESOURCES if r["skill_cluster"] == skill]

    if resource_type:
        resources = [r for r in resources if r["resource_type"] == resource_type]

    if minimum_domain_weight is not None:
        resources = [r for r in resources if r["domain_weight"] >= minimum_domain_weight]

    results = []
    ranking_mode = None

    for r in resources:
        score, mode = rank_resource(r)
        r["score"] = score
        results.append(r)
        ranking_mode = ranking_mode or mode

    results.sort(key=lambda x: x["score"], reverse=True)

    total = len(results)
    page = results[offset : offset + limit]

    return {
        "skill_cluster": skill,
        "results": page,
        "count": total,
        "total_results": total,
        "ranking_mode": ranking_mode,
    }
