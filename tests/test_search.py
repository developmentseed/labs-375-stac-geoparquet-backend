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
    assert response.json()["features"][0]["id"] == "ne_m_4110264_sw_13_060_20220827"
    next_link = next(
        (link for link in response.json()["links"] if link["rel"] == "next")
    )
    url = urllib.parse.urlparse(next_link["href"])
    assert urllib.parse.parse_qs(url.query) == {"limit": ["1"], "offset": ["1"]}
    response = client.get("/search", params=url.query)
    assert response.status_code == 200
    assert response.json()["features"][0]["id"] == "ne_m_4110263_sw_13_060_20220820"
