import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_task(client):
    resp = await client.post("/tasks/", json={"title": "Test task"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test task"
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_tasks(client):
    await client.post("/tasks/", json={"title": "Task 1"})
    await client.post("/tasks/", json={"title": "Task 2"})
    resp = await client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


@pytest.mark.asyncio
async def test_get_task(client):
    create = await client.post("/tasks/", json={"title": "Get me"})
    task_id = create.json()["id"]
    resp = await client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Get me"


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    resp = await client.get("/tasks/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client):
    create = await client.post("/tasks/", json={"title": "Old title"})
    task_id = create.json()["id"]
    resp = await client.put(f"/tasks/{task_id}", json={"title": "New title", "status": "done"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New title"
    assert resp.json()["status"] == "done"


@pytest.mark.asyncio
async def test_update_task_not_found(client):
    resp = await client.put("/tasks/99999", json={"title": "Nope"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_task(client):
    create = await client.post("/tasks/", json={"title": "Delete me"})
    task_id = create.json()["id"]
    resp = await client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    get_resp = await client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client):
    resp = await client.delete("/tasks/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_task_invalid_status(client):
    resp = await client.post("/tasks/", json={"title": "Bad", "status": "invalid"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_task_empty_title(client):
    resp = await client.post("/tasks/", json={"title": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "app" in resp.json()
