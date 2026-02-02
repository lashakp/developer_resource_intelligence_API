import joblib
import pathlib
from typing import Optional

# Resolve path relative to this file
MODEL_PATH = pathlib.Path(__file__).parent / "linear_ranker.pkl"

_model: Optional[object] = None


def _load_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model


def extract_features(resource):
    return [
        resource.get("domain_weight", 0),
        1 if resource.get("is_github") else 0,
        1 if resource.get("resource_type") == "tool" else 0,
        1 if resource.get("resource_type") == "documentation" else 0,
    ]


def predict_score(resource) -> float:
    model = _load_model()
    if model is None:
        raise RuntimeError("ML model not available")
    return float(model.predict([extract_features(resource)])[0])


def model_available() -> bool:
    return MODEL_PATH.exists()
