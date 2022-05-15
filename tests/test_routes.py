import pytest

from fastapi.testclient import TestClient

from app.db.repositories import AnalystRepository
from app.api.routes import api_prefix


# TODO: split out subtests into @pytest.mark.parametrize tests
@pytest.mark.analyst
def test_create_analyst(test_client: TestClient) -> None:
    response = test_client.post(f"{api_prefix}/analysts")
    assert response.status_code != 200
    assert 'field required' in str(response.json().get('detail'))

    response = test_client.post(f"{api_prefix}/analysts", json={
        "name": "TestAnalyst",
        "company": "TestCorp"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "TestAnalyst"
    assert response.json()["company"] == "TestCorp"
    assert response.json()["id"] > 0


@pytest.mark.analyst
def test_get_analysts(test_client: TestClient) -> None:
    response = test_client.get(f"{api_prefix}/analysts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.analyst
def test_read_analyst(test_client: TestClient):
    response = test_client.get(f"{api_prefix}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "TestCorp"}


@pytest.mark.analyst
def test_update_analyst(test_client: TestClient):
    response = test_client.get(f"{api_prefix}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "TestCorp"}

    response = test_client.put(f"{api_prefix}/analysts/1",
                               json={"id": 1, "name": "TestAnalyst", "company": "Test Corp"})
    # assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "Test Corp"}


@pytest.mark.analyst
def test_delete_analyst(test_client: TestClient):
    response = test_client.delete(f"{api_prefix}/analysts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "TestAnalyst", "company": "Test Corp"}

    response = test_client.delete(f"{api_prefix}/analysts/1")
    assert response.status_code == 404


