import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db


def test_get_db(db):
    session = next(get_db())
    assert isinstance(session, Session)
    session.close()


def test_get_current_user_valid_token(db, mock_oauth2_token, mock_user, mocker):
    mocker.patch("app.dependencies.decode_token", return_value=mock_user)

    user = get_current_user(token=mock_oauth2_token, db=db)

    assert user == mock_user


def test_get_current_user_invalid_token(db, mock_oauth2_token, mocker):
    mocker.patch("app.dependencies.decode_token", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=mock_oauth2_token, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"
