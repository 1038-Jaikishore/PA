import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data

def test_get_patients_list():
    with TestClient(app) as client:
        response = client.get("/api/patients?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "patients" in data
        assert "total" in data

def test_get_unknown_patient():
    with TestClient(app) as client:
        response = client.get("/api/patients/UNKNOWN_PATIENT_123")
        assert response.status_code == 404

def test_get_unknown_patient_context():
    with TestClient(app) as client:
        response = client.get("/api/patients/UNKNOWN_PATIENT_123/clinical-context")
        assert response.status_code == 404
