from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, database, oauth2, models
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.user_id
    )
    vote_found = vote_query.first()

    if vote.dir == 1:
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user has already voted on post with id {vote.post_id}"
            )
        db.add(models.Vote(post_id=vote.post_id, user_id=current_user.user_id))
    else:
        if not vote_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user hasn't voted on post"
            )
        vote_query.delete(synchronize_session=False)

    db.commit()
    return {"message": "vote registered" if vote.dir == 1 else "vote removed"}
