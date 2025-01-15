from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResp(UserBase):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    id: int


class Token(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    access_token: str
    token_type: str


class CommentBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    content: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase):

    id: int
    user_id: int
    file_id: int


class FileBase(BaseModel):
    filename: str
    file_type: str
    result_found: bool


class FileCreate(FileBase):
    user_id: int


class FileResp(FileBase):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    id: int
    user_id: int
