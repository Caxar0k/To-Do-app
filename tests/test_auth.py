import pytest


USER_DATA = {
    "username": "test_user",
    "password": "password123",
    "email": "test@example.com",
}


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/user",
        json=USER_DATA,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "User creation successful"


@pytest.mark.asyncio
async def test_login_user(client):
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

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Authorization successful"
    assert data["access_token"]

    assert "my_access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_unknown_user(client):
    response = await client.post(
        "/user/login",
        json={
            "username": "unknown_user",
            "password": "password123",
        },
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Wrong password or login"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/user",
        json=USER_DATA,
    )

    response = await client.post(
        "/user/login",
        json={
            "username": USER_DATA["username"],
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Wrong password or login"


@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    response = await client.post(
        "/user",
        json={
            "username": "test_user",
            "password": "password123",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_username_too_long(client):
    response = await client.post(
        "/user",
        json={
            "username": "a" * 51,
            "password": "password123",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_with_same_name_and_email(client):
    await client.post(
        "/user",
        json=USER_DATA,
    )
    response = await client.post(
        "/user",
        json=USER_DATA,
    )

    assert response.status_code == 409