from typing import Mapping


def compute_score(resource: Mapping) -> float:
    score = float(resource.get("domain_weight", 0))

    if resource.get("is_github"):
        score += 2.0

    if resource.get("resource_type") == "tool":
        score += 1.0
    elif resource.get("resource_type") == "documentation":
        score += 0.5

    return round(score, 2)
