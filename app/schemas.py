
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    # id: int
    title: str
    content: str
    is_published: bool = True


class PostReturn(Post):
    id: int
    pass

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
