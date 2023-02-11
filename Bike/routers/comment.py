from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from handler import get_current_user, raise_404_exception, success_message, token_exception
import models
import uuid

router = APIRouter(
    prefix="/api/comment",
    tags=["Comment"],
    responses={404: {"description": "Not found"}}
)


class Comment(BaseModel):
    description: str = Field(min_length=1)
    bike_id: uuid.UUID


@router.get("/")
async def get_all_comment(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()


@router.get("/{id}")
async def get_comment(id: uuid.UUID, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise raise_404_exception('Comment')
    return comment


@router.post("/")
async def create_comment(comment: Comment, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    comment_model = models.Comment()
    comment_model.bike_id = comment.bike_id
    comment_model.user_id = user.get("id")
    comment_model.description = comment.description
    try:
        db.add(comment_model)
        db.commit()
        db.refresh(comment_model)
        return success_message(201)
    except:
        raise HTTPException(
            status_code=409, detail="This bike doesn't exists!")


@router.put("/{id}")
async def update_comment(id: uuid.UUID, comment: Comment, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    comment_model = db.query(models.Comment).filter(models.Comment.id == id).filter(
        models.Comment.user_id == user.get("id")).first()
    if not comment_model:
        raise raise_404_exception('Comment')
    comment_model.description = comment.description
    try:
        db.add(comment_model)
        db.commit()
        db.refresh(comment_model)
        return success_message(200)
    except:
        raise HTTPException(
            status_code=409, detail="This bike doesn't exists!")


@router.delete("/{id}")
async def delete_comment(id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    comment = db.query(models.Comment).filter(models.Comment.id == id).filter(
        models.Comment.user_id == user.get("id")).first()
    if not comment:
        raise raise_404_exception('Comment')
    db.query(models.Comment).filter(models.Comment.id == id).filter(
        models.Comment.user_id == user.get("id")).delete()
    db.commit()
    return success_message(200)
