from fastapi import FastAPI
from app.routers import auth, vote, user, post
from .database import engine
from app import models
from fastapi.middleware.cors import CORSMiddleware


# use only when alembic not applied
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "'/docs/' in the url to test routes with swagger UI"}
