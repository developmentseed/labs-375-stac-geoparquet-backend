import urllib.parse

from fastapi.testclient import TestClient


async def test_get_search(client: TestClient) -> None:
    response = client.get("/search")
    assert response.status_code == 200, response.text


async def test_post_search(client: TestClient) -> None:
    response = client.post("/search", json={})
    assert response.status_code == 200, response.text


async def test_paging(client: TestClient) -> None:
    params = {"limit": 1}
    response = client.get("/search", params=params)
    assert response.status_code == 200
    next_link = next(
        (link for link in response.json()["links"] if link["rel"] == "next")
    )
    url = urllib.parse.urlparse(next_link["href"])
    print(url.params)
    params.update(url.params)
