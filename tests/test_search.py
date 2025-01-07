from fastapi.testclient import TestClient


async def test_get_search(client: TestClient) -> None:
    response = client.get("/search")
    assert response.status_code == 200, response.text


async def test_post_search(client: TestClient) -> None:
    response = client.post("/search", json={})
    assert response.status_code == 200, response.text
