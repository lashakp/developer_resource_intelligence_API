import joblib
from pathlib import Path
from fastapi.testclient import TestClient
import api.ml.ranker as ranker


class DummyModel:
    def predict(self, X):
        return [1.23]


def test_recommendations_returns_rule_when_no_model(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(ranker, "MODEL_PATH", tmp_path / "linear_ranker.pkl")
    if ranker.MODEL_PATH.exists():
        ranker.MODEL_PATH.unlink()
    monkeypatch.setattr(ranker, "_model", None)

    from api.main import app
    client = TestClient(app)

    resp = client.get("/v1/recommendations", params={"skill": "backend", "limit": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ranking_mode"] == "rule"
    assert "results" in data


def test_recommendations_returns_ml_when_model_present(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(ranker, "MODEL_PATH", tmp_path / "linear_ranker.pkl")
    joblib.dump(DummyModel(), ranker.MODEL_PATH)
    monkeypatch.setattr(ranker, "_model", None)

    from api.main import app
    client = TestClient(app)

    resp = client.get("/v1/recommendations", params={"skill": "backend", "limit": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ranking_mode"] == "ml"
    assert "results" in data