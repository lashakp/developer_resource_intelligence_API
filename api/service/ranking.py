from typing import Tuple

from api.ml.ranker import predict_score, model_available
from api.service.scoring import compute_score


def rank_resource(resource: dict, allow_ml: bool = True) -> Tuple[float, str]:
    """
    Rank a single resource.

    Returns:
        (score, ranking_mode)
        ranking_mode ∈ {"ml", "rule"}
    """

    if allow_ml and model_available():
        try:
            return predict_score(resource), "ml"
        except Exception:
            # Safe fallback if model fails
            return compute_score(resource), "rule"

    return compute_score(resource), "rule"
