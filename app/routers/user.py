from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app import utils, models
from app.database import get_db
from app import models
from app.schemas import UserResponse, User

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):
    user.password = utils.hash_function(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/getuser/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return user
