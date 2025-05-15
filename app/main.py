from fastapi import Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session
from app import models

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


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


@app.get("/")
def root():
    return {"message": "welcome to my [first] api"}


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where post_id = %s""", (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} not found")
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    # using raw sql to fetch data
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()  # using sqlalchemy orm
    return {"posts": posts}


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """delete from posts where post_id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""insert into posts (title, content, is_published) values (%s, %s, %s) returning * """,
    #                (post.title, post.content, post.is_published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())  # using the orm
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""update posts set title = %s, content = %s, is_published = %s where post_id = %s returning * """,
    #                (post.title, post.content, post.is_published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
