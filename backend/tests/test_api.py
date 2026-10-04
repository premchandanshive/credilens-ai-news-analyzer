"""
CrediLens — API End-to-End & Integration Tests
"""

import pytest
from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert data["error"] is None

def test_system_status_endpoint():
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "models" in data["data"]
    assert "database" in data["data"]

def test_auth_flow():
    # 1. Login with demo seed user
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "demo@credilens.local", "password": "demo1234"}
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["success"] is True
    token = login_data["data"]["token"]
    assert token is not None

    # 2. Get profile with Bearer token
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["success"] is True
    assert me_data["data"]["email"] == "demo@credilens.local"

def test_analyze_text_endpoint():
    payload = {
        "title": "NASA Artemis Program Propulsion Test",
        "text": "NASA engineers successfully completed a full-duration 500-second hot fire test of the Space Launch System core stage at Stennis Space Center. All four RS-25 engines fired producing two million pounds of thrust."
    }
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    
    assert "id" in res
    assert "credibilityScore" in res
    assert "credibilityBand" in res
    assert "componentScores" in res
    assert "claims" in res
    assert "sources" in res
    assert "languageAnalysis" in res
    assert "explanation" in res
    assert len(res["claims"]) > 0

    # Test retrieving analysis detail
    analysis_id = res["id"]
    detail_resp = client.get(f"/api/analysis/{analysis_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["data"]["id"] == analysis_id

    # Test history list
    hist_resp = client.get("/api/analysis/history")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()["data"]
    assert hist_data["total"] >= 1
    assert any(item["id"] == analysis_id for item in hist_data["items"])

    # Test report generation
    rep_resp = client.get(f"/api/analysis/{analysis_id}/report")
    assert rep_resp.status_code == 200
    assert rep_resp.json()["data"]["reportId"].startswith("REP-")
