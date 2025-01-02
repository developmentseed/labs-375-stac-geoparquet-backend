from fastapi.testclient import TestClient


async def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
