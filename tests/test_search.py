from fastapi.testclient import TestClient


async def test_get_search(client: TestClient) -> None:
    response = client.get("/search")
    assert response.status_code == 200


async def test_post_search(client: TestClient) -> None:
    response = client.post("/search")
    assert response.status_code == 200
