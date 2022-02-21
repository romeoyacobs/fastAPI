from curses.ascii import HT
from .. import models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.oath2 import get_current_user

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/") # TODO: response_model=schemas.Vote
async def vote_post(voting_data: schemas.Vote, db: Session = Depends(get_db), current_user: models.User  = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == voting_data.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {voting_data.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == voting_data.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if voting_data.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} has already voted on post with id {voting_data.post_id}")
        
        new_vote = models.Vote(post_id=voting_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        #db.refresh(new_vote)
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} has not voted on post with id {voting_data.post_id}")
        
        vote_query.delete()
        db.commit()
        return {"message": "Successfully removed vote"}
