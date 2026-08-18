import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_resolve_policy_missing_inputs():
    with TestClient(app) as client:
        response = client.post("/api/policies/resolve", json={
            "icd10": "",
            "hcpcs_cpt": ""
        })
        assert response.status_code == 400 # Our custom validation in the route
        
        response2 = client.post("/api/policies/resolve", json={
            "icd10": "M17.11"
        })
        assert response2.status_code == 422 # Pydantic missing field

def test_resolve_policy_valid_format():
    with TestClient(app) as client:
        response = client.post("/api/policies/resolve", json={
            "icd10": "M17.11",
            "hcpcs_cpt": "97110"
        })
        assert response.status_code == 200
        data = response.json()
        assert "inputs" in data
        assert data["inputs"]["icd10"] == "M17.11"
        assert data["inputs"]["normalized_icd10"] == "M1711"
        assert data["inputs"]["normalized_hcpcs"] == "97110"
        
        assert "intermediate_results" in data
        assert "resolved_policies" in data
        assert "covered" in data["resolved_policies"]
        assert "non_covered" in data["resolved_policies"]
        assert data["jurisdiction_status"] == "NOT_AVAILABLE_IN_CURRENT_DATASET"

def test_resolve_policy_with_dots():
    with TestClient(app) as client:
        response = client.post("/api/policies/resolve", json={
            "icd10": "A15.0",
            "hcpcs_cpt": " 99213 "
        })
        assert response.status_code == 200
        data = response.json()
        assert data["inputs"]["normalized_icd10"] == "A150"
        assert data["inputs"]["normalized_hcpcs"] == "99213"
