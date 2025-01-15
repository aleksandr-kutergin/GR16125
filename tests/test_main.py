from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app import models, schemas


@pytest.mark.asyncio
async def test_create_user(client: TestClient, mock_db):
    new_user_data = {
        "email": "new_user@example.com",
        "password": "password123",
    }

    with patch("app.crud.get_user_by_email", return_value=None):
        with patch(
            "app.crud.create_user", return_value=schemas.UserResp(id=1, **new_user_data)
        ):
            response = client.post("/users/", json=new_user_data)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": new_user_data["email"],
    }


@pytest.mark.asyncio
async def test_create_user_with_existing_email(client: TestClient, mock_db):
    existing_user_data = {
        "email": "existing_user@example.com",
        "password": "password123",
    }
    with patch(
        "app.crud.get_user_by_email", return_value=models.User(**existing_user_data)
    ):
        response = client.post("/users/", json=existing_user_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_login_for_access_token_success(client: TestClient):
    form_data = {"username": "test@example.com", "password": "test"}

    user_mock = MagicMock()
    user_mock.email = form_data["username"]
    user_mock.password = "$2b$12$EmwlGZjQAxZLkXee.6YK3uMceliCY2yukxoS2aNQ5Hr7KHylaN80K"

    with patch("app.crud.get_user_by_email", return_value=user_mock):
        with patch("app.auth.verify_password", return_value=True):
            response = client.post("/token", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials(client: TestClient):
    form_data = {"username": "test@example.com", "password": "wrongpassword"}

    user_mock = MagicMock()
    user_mock.email = form_data["username"]
    user_mock.password = "$2b$12$kzlv5wkm.f5xg1xlbHp7Jf1a3XApOBVQOLB.r/.z6Q8MdlhtlaGZa"

    with patch("app.crud.get_user_by_email", return_value=user_mock):
        with patch("app.auth.verify_password", return_value=False):
            response = client.post("/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
