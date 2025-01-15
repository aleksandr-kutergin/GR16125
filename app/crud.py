from fastapi import HTTPException
from sqlalchemy.orm import Session

from .auth import hash_password
from .models import Comment, File, User
from .schemas import CommentCreate, FileCreate, UserCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def save_file(db: Session, file_data: FileCreate):
    db_file = File(**file_data.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.id


def add_comment(db: Session, comment_data: CommentCreate, file_id: int, user_id: int):
    if not (file := db.query(File).filter(File.id == file_id).first()):
        raise HTTPException(status_code=404, detail="File not found")
    db_comment = Comment(**comment_data.model_dump(), file_id=file_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
