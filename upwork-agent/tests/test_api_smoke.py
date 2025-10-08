"""API smoke tests for the Upwork proposal agent.

These tests verify that the FastAPI application exposes a healthy
heartbeat endpoint at `/healthz` and that the `/generate` endpoint
returns the expected shape (proposal_md and fit_score fields) using
FastAPI's TestClient. The tests intentionally avoid any network I/O
and operate purely on the in-memory app instance.
"""

from fastapi.testclient import TestClient
from server import app


def test_healthz() -> None:
    """Ensure the /healthz endpoint returns a 200 and ok True."""
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("ok") is True


def test_generate() -> None:
    """Ensure the /generate endpoint returns a proposal and fit score."""
    client = TestClient(app)
    payload = {
        "job_text": "Title: Build a Python FastAPI agent\nNeed: Python, FastAPI"
    }
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    # response must include proposal and integer fit score
    assert "proposal_md" in data and "fit_score" in data
    assert isinstance(data["fit_score"], int)