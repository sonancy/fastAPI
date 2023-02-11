from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from handler import get_current_user, success_message, token_exception
import models
import uuid

router = APIRouter(
    prefix="/api/like",
    tags=["Like"],
    responses={404: {"description": "Not found"}}
)


class Like(BaseModel):
    bike_id: uuid.UUID


@router.get("/")
def ge_all_liked_bike(db: Session = Depends(get_db)):
    return db.query(models.Like, models.Bike).join(models.Bike).join(models.User).all()


@router.get("/most-liked-bikes")
def get_most_liked_bike(db: Session = Depends(get_db)):
    return db.query(models.Like.bike_id, func.count(models.Like.bike_id).label("total")).group_by(models.Like.bike_id).order_by(desc("total")).all()


@router.post("/")
def like_bike(bike: Like, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    isLiked = db.query(models.Like).filter(
        models.Like.bike_id == bike.bike_id).filter(models.Like.user_id == user.get("id")).first()
    if isLiked is None:
        like_model = models.Like()
        like_model.bike_id = bike.bike_id
        like_model.user_id = user.get("id")
        db.add(like_model)
    else:
        db.query(models.Like).filter(
            models.Like.bike_id == bike.bike_id).delete()
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="Bike doesn't exists"
        )
    return success_message(200)
