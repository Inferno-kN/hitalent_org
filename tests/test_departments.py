import pytest


@pytest.mark.asyncio
async def test_create_department(client):
    response = await client.post("/departments/", json={"name": "IT", "parent_id": None})
    assert response.status_code == 201
    assert response.json()["name"] == "IT"


@pytest.mark.asyncio
async def test_get_department_tree(client):
    await client.post("/departments/", json={"name": "Backend", "parent_id": None})
    response = await client.get("/departments/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Backend"