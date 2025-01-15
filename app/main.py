from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, dependencies, file_processing, models, schemas
from app.auth import create_access_token, verify_password
from app.database import init_db

app = FastAPI()

init_db()


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.UserResp)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/files/upload", response_model=schemas.FileResp)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    if file.filename.endswith(".txt"):
        return await file_processing.process_txt_file(file, db, current_user.id)
    elif file.filename.endswith(".csv"):
        return await file_processing.process_csv_file(file, db, current_user.id)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")


@app.get("/files/", response_model=List[schemas.FileResp])
def get_user_files(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    files = db.query(models.File).filter(models.File.user_id == current_user.id).all()
    return files


@app.post("/files/{file_id}/comments", response_model=schemas.CommentOut)
def add_comment(
    file_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return crud.add_comment(
        db=db, comment_data=comment, file_id=file_id, user_id=current_user.id
    )


@app.get("/files/{file_id}/comments", response_model=List[schemas.CommentOut])
def get_comments_for_file(file_id: int, db: Session = Depends(dependencies.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.file_id == file_id).all()
    return comments
