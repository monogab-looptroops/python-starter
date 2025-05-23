from fastapi.testclient import TestClient
from api.server import get_api

client = TestClient(get_api())


def test_hello_world():
    response = client.get("/hello/world")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_api_user():
    response = client.get("/api/3")
    expected_response = {
        "id": 3,
        "name": "John",
        "dob": "1990-01-01"
    }
    assert response.status_code == 200
    assert response.json() == expected_response
   