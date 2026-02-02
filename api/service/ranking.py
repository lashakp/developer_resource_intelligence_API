from typing import Tuple
from api.ml.ranker import predict_score, model_available
from api.service.scoring import compute_score


def rank_resource(resource) -> Tuple[float, str]:
    if model_available():
        try:
            return predict_score(resource), "ml"
        except Exception:
            return compute_score(resource), "rule"

    return compute_score(resource), "rule"
