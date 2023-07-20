import pytest
from fastapi.testclient import TestClient

from hf_serve.main import app


@pytest.fixture()
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize(
    "path, expected_status, method",
    [
        (
            "/",
            200,
            "post",
        ),
        ("/healthz", 200, "get"),
        ("/readyz", 200, "get"),
    ],
)
def test_endpoint(test_client, path, expected_status, method):
    response = test_client.request(method, path, json={"data": "test"})
    assert response.status_code == expected_status
