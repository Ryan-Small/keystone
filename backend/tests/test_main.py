import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_say_hello_empty_name(client: TestClient) -> None:
    response = client.get("/hello/")
    assert response.status_code == 404


def test_say_hello_with_special_chars(client: TestClient) -> None:
    response = client.get("/hello/Alice%20Smith")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Alice Smith"}
