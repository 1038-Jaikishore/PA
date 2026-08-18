import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.db.mongodb import connect_to_mongo, close_mongo_connection

@pytest_asyncio.fixture(scope="module")
async def client():
    await connect_to_mongo()
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    await close_mongo_connection()

@pytest.mark.asyncio
async def test_get_cases_list(client):
    response = await client.get("/api/prior-auth/cases")
    assert response.status_code == 200
    cases = response.json()
    assert isinstance(cases, list)

@pytest.mark.asyncio
async def test_get_valid_case(client):
    # Fetch all to get one ID
    cases_resp = await client.get("/api/prior-auth/cases")
    cases = cases_resp.json()
    if not cases:
        pytest.skip("No aligned cases found in DB to test.")
    
    case_id = cases[0]["case_id"]
    response = await client.get(f"/api/prior-auth/cases/{case_id}")
    assert response.status_code == 200
    case = response.json()
    assert case["case_id"] == case_id
    assert "patient" in case
    assert "diagnosis" in case
    assert "requested_service" in case

@pytest.mark.asyncio
async def test_resolve_policy_for_case(client):
    cases_resp = await client.get("/api/prior-auth/cases")
    cases = cases_resp.json()
    if not cases:
        pytest.skip("No aligned cases found in DB to test.")
    
    case_id = cases[0]["case_id"]
    response = await client.post(f"/api/prior-auth/cases/{case_id}/resolve-policy")
    assert response.status_code == 200
    resolution = response.json()
    assert "status" in resolution or "jurisdiction_status" in resolution

@pytest.mark.asyncio
async def test_invalid_case_id(client):
    response = await client.get("/api/prior-auth/cases/INVALID_CASE_ID_9999")
    assert response.status_code == 404
