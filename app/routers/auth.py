from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import oauth2
from app.schemas import UserLogin
from app.database import get_db
from app.models import User
from app.utils import verify_password

# set parameter to tags='specific word' to utilize fastapidocs grouping
router = APIRouter()


@router.post("/login")
def authenticate_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid email/password")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid email/password")

    access_token = oauth2.create_access_token(data={"user_id": user.user_id})

    return {"access token": access_token, "token_type": "bearer"}
