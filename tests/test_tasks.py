import pytest


USER_DATA = {
    "username": "test_user",
    "password": "password123",
    "email": "test@example.com",
}


async def create_and_login_user(client):
    await client.post(
        "/user",
        json=USER_DATA,
    )

    response = await client.post(
        "/user/login",
        json={
            "username": USER_DATA["username"],
            "password": USER_DATA["password"],
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_task(client):
    await create_and_login_user(client)

    response = await client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Test description",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Task creation successful"
    assert isinstance(data["task_id"], int)


@pytest.mark.asyncio
async def test_get_tasks(client):
    await create_and_login_user(client)

    await client.post(
        "/tasks",
        json={
            "title": "Task 1",
            "description": "Description 1",
            "completed": False,
        },
    )

    await client.post(
        "/tasks",
        json={
            "title": "Task 2",
            "description": "Description 2",
            "completed": True,
        },
    )

    response = await client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Geting all tasks successful"

    tasks = data["Tasks"]

    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_get_task_by_id(client):
    await create_and_login_user(client)

    create_response = await client.post(
        "/tasks",
        json={
            "title": "My task",
            "description": "Description",
            "completed": False,
        },
    )

    task_id = create_response.json()["task_id"]

    response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["Task_by_id"]["id"] == task_id
    assert data["Task_by_id"]["title"] == "My task"
    assert data["Task_by_id"]["description"] == "Description"
    assert data["Task_by_id"]["completed"] is False


@pytest.mark.asyncio
async def test_get_nonexistent_task(client):
    await create_and_login_user(client)

    response = await client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "No task by this id"


@pytest.mark.asyncio
async def test_update_task(client):
    await create_and_login_user(client)

    create_response = await client.post(
        "/tasks",
        json={
            "title": "Old title",
            "description": "Old description",
            "completed": False,
        },
    )

    task_id = create_response.json()["task_id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New description",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Task editing successful"

    get_response = await client.get(f"/tasks/{task_id}")

    task = get_response.json()["Task_by_id"]

    assert task["title"] == "New title"
    assert task["description"] == "New description"
    assert task["completed"] is True


@pytest.mark.asyncio
async def test_update_nonexistent_task(client):
    await create_and_login_user(client)

    response = await client.put(
        "/tasks/999999",
        json={
            "title": "New title",
            "description": "Description",
            "completed": True,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No task by this id"


@pytest.mark.asyncio
async def test_delete_task(client):
    await create_and_login_user(client)

    create_response = await client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": None,
            "completed": False,
        },
    )

    task_id = create_response.json()["task_id"]

    response = await client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    get_response = await client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_task(client):
    await create_and_login_user(client)

    response = await client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "No task by this id"


@pytest.mark.asyncio
async def test_tasks_require_authentication(client):
    response = await client.get("/tasks")

    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_task_requires_authentication(client):
    response = await client.post(
        "/tasks",
        json={
            "title": "Unauthenticated task",
            "description": "Description",
            "completed": False,
        },
    )

    assert response.status_code in (401, 403)




    

@pytest.mark.asyncio
async def test_user_cannot_access_another_users_task(client):
    first_user = {
        "username": "user1",
        "password": "password123",
        "email": "user1@example.com",
    }

    second_user = {
        "username": "user2",
        "password": "password123",
        "email": "user2@example.com",
    }

    await client.post("/user", json=first_user)

    await client.post(
        "/user/login",
        json={
            "username": first_user["username"],
            "password": first_user["password"],
        },
    )

    response = await client.post(
        "/tasks",
        json={
            "title": "Private task",
            "description": None,
            "completed": False,
        },
    )

    task_id = response.json()["task_id"]

    # Login as second user.
    await client.post("/user", json=second_user)

    await client.post(
        "/user/login",
        json={
            "username": second_user["username"],
            "password": second_user["password"],
        },
    )

    response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_user_cannot_update_another_users_task(client):
    first_user = {
        "username": "user1",
        "password": "password123",
        "email": "user1@example.com",
    }

    second_user = {
        "username": "user2",
        "password": "password123",
        "email": "user2@example.com",
    }

    await client.post("/user", json=first_user)

    await client.post(
        "/user/login",
        json={
            "username": first_user["username"],
            "password": first_user["password"],
        },
    )

    response = await client.post(
        "/tasks",
        json={
            "title": "Old title",
            "description": "Old description",
            "completed": False,
        },
    )

    task_id = response.json()["task_id"]

    # Login as second user.
    await client.post("/user", json=second_user)

    await client.post(
        "/user/login",
        json={
            "username": second_user["username"],
            "password": second_user["password"],
        },
    )

    response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "Description",
            "completed": True,
        }
    )

    assert response.status_code == 404



@pytest.mark.asyncio
async def test_user_cannot_delete_another_users_task(client):
    first_user = {
        "username": "user1",
        "password": "password123",
        "email": "user1@example.com",
    }

    second_user = {
        "username": "user2",
        "password": "password123",
        "email": "user2@example.com",
    }

    await client.post("/user", json=first_user)

    await client.post(
        "/user/login",
        json={
            "username": first_user["username"],
            "password": first_user["password"],
        },
    )

    response = await client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": None,
            "completed": False,
        },
    )

    task_id = response.json()["task_id"]

    # Login as second user.
    await client.post("/user", json=second_user)

    await client.post(
        "/user/login",
        json={
            "username": second_user["username"],
            "password": second_user["password"],
        },
    )

    response = await client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404