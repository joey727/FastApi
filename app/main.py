from fastapi import FastAPI
from app.routers import auth, vote, user, post
from .database import engine
from app import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)
