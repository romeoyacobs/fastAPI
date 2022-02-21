from curses.ascii import HT

from sqlalchemy import func
from .. import models, schemas
from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.oath2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostWithVote])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = ""
    ):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    posts = query.join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return posts

@router.get("/{id}", response_model=schemas.PostWithVote)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    # query = db.query(models.Post)
    # post = query.filter(models.Post.id == id).first()

    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    post = query.join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def add_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User  = Depends(get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.post("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User  = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perform requested action")

    post_dict = post.dict()
    post_dict["owner_id"] = current_user.id
    post_query.update(post_dict)
    db.commit()
    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")
    
    return updated_post

@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User  = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perform requested action")

    post_query.delete()
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.get("/posts")
# async def get_posts(db: Session = Depends(get_db)):
#     try:
#         query = "SELECT * FROM posts;"
#         cur.execute(query)
#         posts = cur.fetchall()
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Try again later")

#     return {"data": posts}

# @app.get("/posts/{id}")
# async def get_posts(id: int, db: Session = Depends(get_db)):
#     try:
#         query = "SELECT * FROM posts WHERE id = %s;"
#         cur.execute(query, (id,))
#         post = cur.fetchone()
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Try again later")

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")

#     return {"data": post}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def add_post(post: Post, db: Session = Depends(get_db)):
#     try:
#         query = "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;"
#         cur.execute(query, (post.title, post.content, post.published))
#         post = cur.fetchone()
#         conn.commit()
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Try again later")

#     return {"data": post}

# @app.post("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
#     try:
#         query = "UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *;"
#         cur.execute(query, (post.title, post.content, post.published, id))
#         post = cur.fetchone()
#         conn.commit()
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Try again later")

#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")
    
#     return {"data": post}

# @app.delete("/posts/{id}")
# async def delete_post(id: int, db: Session = Depends(get_db)):
#     try:
#         query = "DELETE FROM posts WHERE id = %s RETURNING *;"
#         cur.execute(query, (id,))
#         post = cur.fetchone()
#         conn.commit()
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Try again later")

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)