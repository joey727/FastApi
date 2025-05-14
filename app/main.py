from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
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
    is_published: bool = True


@app.get("/")
def root():
    return {"message": "welcome to my [first] api"}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("""select * from posts where post_id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@app.get("/posts")
def get_all_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """delete from posts where post_id = %s returning * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""insert into posts (title, content, is_published) values (%s, %s, %s) returning * """,
                   (post.title, post.content, post.is_published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""update posts set title = %s, content = %s, is_published = %s where post_id = %s returning * """,
                   (post.title, post.content, post.is_published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return updated_post
