import joblib
import pytest
from pathlib import Path

from api.service.ranking import rank_resource
import api.ml.ranker as ranker
import api.service.scoring as scoring


class DummyModel:
    def predict(self, X):
        return [1.23]


def test_rank_resource_falls_back_to_rule(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(ranker, "MODEL_PATH", tmp_path / "linear_ranker.pkl")
    if ranker.MODEL_PATH.exists():
        ranker.MODEL_PATH.unlink()
    monkeypatch.setattr(ranker, "_model", None)
    monkeypatch.setattr(scoring, "compute_score", lambda r: 0.5)

    score, mode = rank_resource({"domain_weight": 5})
    assert mode == "rule"
    assert score == 0.5


def test_rank_resource_uses_ml_when_available(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(ranker, "MODEL_PATH", tmp_path / "linear_ranker.pkl")
    joblib.dump(DummyModel(), ranker.MODEL_PATH)
    monkeypatch.setattr(ranker, "_model", None)
    monkeypatch.setattr(scoring, "compute_score", lambda r: 0.5)

    score, mode = rank_resource({"domain_weight": 5})
    assert mode == "ml"
    assert pytest.approx(score) == 1.23