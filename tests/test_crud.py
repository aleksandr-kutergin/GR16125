import pytest
from fastapi import HTTPException

from app.auth import hash_password
from app.crud import add_comment, create_user, get_user_by_email, save_file
from app.models import File
from app.schemas import CommentCreate, FileCreate, UserCreate


def test_create_user(db):
    user_data = UserCreate(email="test@test.com", password="testpassword")
    new_user = create_user(db, user_data)

    assert new_user.email == "test@test.com"
    assert new_user.password != "testpassword"
    assert hash_password("testpassword") != new_user.password


def test_get_user_by_email(db):
    if not (user := get_user_by_email(db, "test@test.com")):
        user_data = UserCreate(email="test@test.com", password="testpassword")
        create_user(db, user_data)

    assert user.email == "test@test.com"


def test_get_user_by_email_not_found(db):
    user = get_user_by_email(db, "nonexistent@test.com")

    assert user is None


def test_save_file(db):
    file_data = FileCreate(
        filename="test_file.txt",
        file_type="txt",
        result_found=False,
        user_id=1,
    )
    file_id = save_file(db, file_data)

    saved_file = db.query(File).filter(File.id == file_id).first()
    assert saved_file is not None
    assert saved_file.filename == "test_file.txt"


def test_add_comment(db):
    user_data = UserCreate(email="user@example.com", password="password")
    user = create_user(db, user_data)

    file_data = FileCreate(
        filename="test_file.txt", file_type="txt", result_found=False, user_id=user.id
    )
    file_id = save_file(db, file_data)

    comment_data = CommentCreate(content="This is a test comment")
    comment = add_comment(db, comment_data, file_id=file_id, user_id=user.id)

    assert comment.content == "This is a test comment"
    assert comment.file_id == file_id
    assert comment.user_id == user.id


def test_add_comment_invalid_file(db):
    if not (user := get_user_by_email(db, "test@test.com")):
        user_data = UserCreate(email="test@test.com", password="testpassword")
        user_id = create_user(db, user_data)
    else:
        user_id = user.id

    comment_data = CommentCreate(content="Invalid comment")
    with pytest.raises(HTTPException, match="File not found"):
        add_comment(db, comment_data, file_id=999, user_id=user_id)
