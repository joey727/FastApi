from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# class OwnerResponse(BaseModel):
#     email: EmailStr


class PostReturn(Post):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int

    @field_validator("dir")
    def validate_dir(cls, value):
        if value not in (0, 1):
            raise ValueError("dir must be 0 or 1")
        return value
