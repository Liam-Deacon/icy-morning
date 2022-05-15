import pytest

import datetime

from fastapi.testclient import TestClient

from app.api.routes.v1 import API_PREFIX


# TODO: split out subtests into @pytest.mark.parametrize tests
@pytest.mark.analyst
def test_create_analyst(test_client: TestClient) -> None:
    response = test_client.post(f"{API_PREFIX}/analysts")
    assert response.status_code != 200
    assert "field required" in str(response.json().get("detail"))

    response = test_client.post(
        f"{API_PREFIX}/analysts", json={"name": "TestAnalyst", "company": "TestCorp"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "TestAnalyst"
    assert response.json()["company"] == "TestCorp"
    assert response.json()["id"] > 0


@pytest.mark.analyst
def test_get_analysts(test_client: TestClient) -> None:
    response = test_client.get(f"{API_PREFIX}/analysts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.analyst
def test_read_analyst(test_client: TestClient):
    response = test_client.get(f"{API_PREFIX}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "TestCorp"}


@pytest.mark.analyst
def test_update_analyst(test_client: TestClient):
    response = test_client.get(f"{API_PREFIX}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "TestCorp"}

    response = test_client.put(
        f"{API_PREFIX}/analysts/1",
        json={"id": 1, "name": "TestAnalyst", "company": "Test Corp"},
    )
    # assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "Test Corp"}


@pytest.mark.analyst
def test_delete_analyst(test_client: TestClient):
    response = test_client.delete(f"{API_PREFIX}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "Test Corp"}

    response = test_client.delete(f"{API_PREFIX}/analysts/1")
    assert response.status_code == 404


MOCK_ASSET = {
    "name": "TestAsset",
    "description": "My Test Asset",
    "analyst_id": 1,
    "is_active": True,
    "inception_date": datetime.date.today().isoformat(),
}

# TODO: split out subtests into @pytest.mark.parametrize tests
@pytest.mark.asset
def test_create_asset(test_client: TestClient) -> None:
    response = test_client.post(f"{API_PREFIX}/assets")
    assert response.status_code != 200
    assert "field required" in str(response.json().get("detail"))

    payload = MOCK_ASSET

    response = test_client.post(f"{API_PREFIX}/assets", json=payload)
    assert response.status_code == 201
    assert response.json() == {**payload, **{"id": 1}}


@pytest.mark.asset
def test_get_assets(test_client: TestClient) -> None:
    response = test_client.get(f"{API_PREFIX}/assets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asset
def test_read_asset(test_client: TestClient):
    response = test_client.get(f"{API_PREFIX}/assets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, **MOCK_ASSET}


@pytest.mark.asset
def test_update_asset(test_client: TestClient):
    response = test_client.get(f"{API_PREFIX}/assets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, **MOCK_ASSET}

    payload = {"id": 1, **MOCK_ASSET, **{"description": "TBD"}}

    response = test_client.put(f"{API_PREFIX}/assets/1", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


@pytest.mark.asset
def test_delete_asset(test_client: TestClient):
    response = test_client.delete(f"{API_PREFIX}/assets/1")
    assert response.status_code == 200

    response = test_client.delete(f"{API_PREFIX}/assets/1")
    assert response.status_code == 404
