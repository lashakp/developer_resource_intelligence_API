from typing import List, Dict


def demo_recommendations(results: List[Dict]) -> Dict:
    """
    Shape demo-mode recommendations to match RecommendationResponse schema.
    """

    return {
        "mode": "demo",
        "skill_cluster": results[0]["skill_cluster"] if results else None,
        "results": results,
        "count": len(results),
        "total_results": len(results),
        "ranking_mode": "deterministic",
    }
