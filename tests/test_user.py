import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_get_existed_user(client):
    response = await client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


@pytest.mark.anyio
async def test_get_nonexistent_user(client):
    response = await client.get("/users/99999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_user(client):
    payload = {"name": "Test User", "email": "test@example.com"}
    response = await client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


@pytest.mark.anyio
async def test_update_user(client):
    payload = {"name": "Updated User", "email": "updated@example.com"}
    response = await client.put("/users/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]


@pytest.mark.anyio
async def test_delete_user(client):
    response = await client.delete("/users/1")
    assert response.status_code == 204
