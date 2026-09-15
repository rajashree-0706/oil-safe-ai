import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import init_db, SessionLocal
from app.database.seed_data import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()
    db = SessionLocal()
    seed_database(db)
    db.close()

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OPERATIONAL"

def test_login_and_roles():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "Admin@2026"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["role"] == "Admin"

def test_get_incidents_and_analysis():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert len(incidents) >= 1

    unit3_id = incidents[0]["id"]
    analysis_res = client.get(f"/api/incidents/{unit3_id}/analyze")
    assert analysis_res.status_code == 200
    analysis = analysis_res.json()

    assert analysis["risk_score"] == 87.0
    assert analysis["risk_level"] == "CRITICAL"
    assert analysis["sif_precursor"] is True
    assert analysis["confidence"] == 0.94

    violation_rules = [v["rule"] for v in analysis["lsr_violations"]]
    assert "LSR #1" in violation_rules
    assert "LSR #3" in violation_rules
    assert "LSR #5" in violation_rules

def test_dashboard_metrics():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "risk_trend" in data
    assert "department_data" in data

def test_heatmap_data():
    response = client.get("/api/risk/heatmap")
    assert response.status_code == 200
    heatmap = response.json()
    assert len(heatmap) >= 1
    assert any(h["code"] == "LOC-U3" for h in heatmap)

def test_report_export_json_and_html():
    response_json = client.get("/api/reports/1/json")
    assert response_json.status_code == 200
    assert response_json.json()["risk_score"] == 87.0

    response_html = client.get("/api/reports/1/html")
    assert response_html.status_code == 200
    assert "OIL-SAFE AI" in response_html.text

def test_safety_copilot_query():
    response = client.post("/api/copilot/query", json={"query": "Why was this incident classified as SIF?", "incident_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert "SIF Precursor" in data["answer"]
    assert data["confidence"] >= 0.90
    assert len(data["evidence"]) >= 1

def test_analytics_and_anomalies():
    res_anom = client.get("/api/analytics/anomalies")
    assert res_anom.status_code == 200
    assert len(res_anom.json()) >= 1

    res_fore = client.get("/api/analytics/forecast")
    assert res_fore.status_code == 200
    assert len(res_fore.json()) >= 1

