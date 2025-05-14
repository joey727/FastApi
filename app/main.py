from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


app = FastAPI()

try:
    conn = connect(host="localhost", database="myFastApi",
                   user="postgres", password="rootAdmin", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection succesfull")
except Exception as err:
    print("problem with connection")
    print(err)


class Post(BaseModel):
    title: str
    content: str
    is_published: bool
    rating: Optional[int] = None


my_posts = [{"title": "first post",
             "content": "something interesting", "id": 1}]

# search for post by id


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

# add posts


def add_post(post: Post):
    my_posts.append(post)


@app.get("/")
def root():
    return {"message": "welcome to my [first] api"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}
