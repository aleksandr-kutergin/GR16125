from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import decode_token, oauth2_scheme
from .database import SessionLocal
from .models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    if not (user := decode_token(token, db)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user
