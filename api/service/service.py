from typing import List, Dict
from collections import Counter
import os

from fastapi import HTTPException

from api.data import RESOURCES
from api.service.ranking import rank_resource
from api.service.demo import demo_recommendations


# =========================================================
# Config
# =========================================================

ENABLE_DEMO = os.getenv("ENABLE_DEMO", "true").lower() == "true"

# =========================================================
# Limits
# =========================================================

DEMO_MAX_RESULTS = 8
FULL_MAX_RESULTS = 50


# =========================================================
# Discovery / Metadata
# =========================================================

def get_available_skills() -> List[str]:
    return sorted({r["skill_cluster"] for r in RESOURCES})


def get_available_resource_types() -> List[str]:
    return sorted({r["resource_type"] for r in RESOURCES})


def get_filter_availability() -> Dict[str, List[str]]:
    availability: Dict[str, set] = {}
    for r in RESOURCES:
        availability.setdefault(r["skill_cluster"], set()).add(r["resource_type"])
    return {k: sorted(v) for k, v in availability.items()}


def get_available_domains() -> List[Dict]:
    counter = Counter(r["domain"] for r in RESOURCES)
    return [{"domain": d, "count": c} for d, c in counter.most_common()]


def get_stats(top_n: int = 5) -> Dict:
    skill_counts = Counter(r["skill_cluster"] for r in RESOURCES)
    domain_counts = Counter(r["domain"] for r in RESOURCES)
    resource_type_counts = Counter(r["resource_type"] for r in RESOURCES)

    return {
        "total_resources": len(RESOURCES),
        "top_skills": [
            {"skill_cluster": skill, "count": count}
            for skill, count in skill_counts.most_common(top_n)
        ],
        "top_domains": [
            {"domain": domain, "count": count}
            for domain, count in domain_counts.most_common(top_n)
        ],
        "resource_types": [
            {"resource_type": rtype, "count": count}
            for rtype, count in resource_type_counts.most_common()
        ],
    }


# =========================================================
# Core Recommendations Logic
# =========================================================

def get_recommendations(
    skill: str,
    limit: int = 5,
    offset: int = 0,
    resource_type: str | None = None,
    minimum_domain_weight: int | None = None,
    access_mode: str = "demo",
):
    """
    Returns ranked recommendations based on access mode.

    demo:
        - deterministic ranking
        - capped results
        - no ML
    full:
        - ML ranking when available
        - full pagination
    """

    is_demo = access_mode == "demo"

    # -----------------------------------------------------
    # Filter
    # -----------------------------------------------------

    normalized_skill = skill.strip().lower()

    normalized_resource_type = (
        resource_type.strip().lower()
        if resource_type
        else None
    )

    filtered = [
        r for r in RESOURCES
        if r["skill_cluster"].lower() == normalized_skill
    ]

    if normalized_resource_type:
        filtered = [
            r for r in filtered
            if r["resource_type"].lower() == normalized_resource_type
        ]

    if minimum_domain_weight is not None:
        filtered = [
            r for r in filtered
            if r["domain_weight"] >= minimum_domain_weight
        ]

    if not filtered:
        return {
            "mode": access_mode,
            "skill_cluster": skill,
            "results": [],
            "count": 0,
            "total_results": 0,
            "ranking_mode": None,
        }

    # -----------------------------------------------------
    # Rank
    # -----------------------------------------------------

    results = []
    ranking_mode = None

    if access_mode == "full":
        ranked = []

        for r in filtered:
            score, mode = rank_resource(r)
            ranking_mode = mode

            r_with_score = r.copy()
            r_with_score["score"] = score

            ranked.append((r_with_score, score))

        ranked.sort(key=lambda x: x[1], reverse=True)
        results = [r for r, _ in ranked]

    else:
        # Demo mode: deterministic, no ML
        results = sorted(
            filtered,
            key=lambda r: (-r["domain_weight"], r["resource_id"])
        )

        results = [
            {**r, "score": None}
            for r in results
        ]

        ranking_mode = "deterministic"

    # -----------------------------------------------------
    # Pagination (authoritative limits)
    # -----------------------------------------------------

    effective_limit = (
        DEMO_MAX_RESULTS if is_demo else min(limit, FULL_MAX_RESULTS)
    )

    total = len(results)
    page = results[offset: offset + effective_limit]

    # -----------------------------------------------------
    # Demo shaping
    # -----------------------------------------------------

    if is_demo:
        if not ENABLE_DEMO:
            raise HTTPException(status_code=401, detail="Demo mode disabled")

        return demo_recommendations(page)

    # -----------------------------------------------------
    # Full response
    # -----------------------------------------------------

    return {
        "mode": "full",
        "skill_cluster": skill,
        "results": page,
        "count": len(page),
        "total_results": total,
        "ranking_mode": ranking_mode,
    }
