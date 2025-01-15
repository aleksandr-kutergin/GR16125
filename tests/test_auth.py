import pytest
from jose import jwt

from app.auth import (create_access_token, decode_token, hash_password,
                      pwd_context, verify_password)


def test_hash_password():
    password = "testpassword"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert pwd_context.verify(password, hashed_password)


def test_verify_password():
    password = "testpassword"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


@pytest.mark.skip("some token issue")
def test_create_access_token(mock_env_variables):
    token = create_access_token({"sub": "test@test.com"})

    decoded_token = jwt.decode(token, "testsecret", algorithms=["HS256"])
    assert decoded_token.get("sub") == "test@test.com"
    assert "exp" in decoded_token


def test_decode_token_valid(mock_db, mock_user, mock_env_variables):
    token = create_access_token({"sub": "test@example.com"})

    mock_db.query().filter().first.return_value = mock_user

    user = decode_token(token, mock_db)

    assert user == mock_user
    mock_db.query().filter().first.assert_called_once()


def test_decode_token_invalid_user(mock_db, mock_env_variables):
    invalid_token = create_access_token({"sub": "wrong@example.com"})

    mock_db.query().filter().first.return_value = None

    user = decode_token(invalid_token, mock_db)

    assert user is None


def test_decode_token_invalid(mock_db, mock_env_variables):
    invalid_token = "invalid.token.string"

    user = decode_token(invalid_token, mock_db)

    assert user is None


def test_decode_token_missing_sub(mock_db, mock_env_variables):
    token = jwt.encode({"exp": 1000}, "testsecret", algorithm="HS256")

    user = decode_token(token, mock_db)

    assert user is None
