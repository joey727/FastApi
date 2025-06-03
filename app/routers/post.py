from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status, APIRouter
from app import models, oauth2
from app.database import get_db
from app.schemas import Post, PostReturn, PostWithVote

router = APIRouter(
    prefix="/posts"
)


@router.get("/{id}", response_model=PostWithVote)
def get_post_by_id(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where post_id = %s""", (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} not found")
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                      isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@router.get("/", response_model=List[PostWithVote])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # using raw sql to fetch data
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    # using sqlalchemy orm
    # adding votes count to post query
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
                                                                                           search)).limit(limit).offset(skip).all()
    return posts


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """delete from posts where post_id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = delete_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if deleted_post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform request")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostReturn)
def create_post(post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, is_published) values (%s, %s, %s) returning * """,
    #                (post.title, post.content, post.is_published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.model_dump(),
                           owner_id=current_user.user_id)  # using the orm
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=PostReturn)
def update_post(id: int, post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, is_published = %s where post_id = %s returning * """,
    #                (post.title, post.content, post.is_published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if updated_post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform request")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post
