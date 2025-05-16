from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session
from app import models, utils
from .routers import user, post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    conn = connect(host="localhost", database="myFastApi",
                   user="postgres", password="rootAdmin", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection succesfull")
except Exception as err:
    print("problem with connection")
    print(err)

app.include_router(user.router)
app.include_router(post.router)
