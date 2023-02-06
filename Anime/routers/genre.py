from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal
from handlers import success_message, get_current_user, raise_404_exception, get_user_exception
import models

router = APIRouter(
    prefix="/genre",
    tags=["Genre"],
    responses={404: {"detail": "Genre not found!"}}
)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


class Genre(BaseModel):
    name: str

    class Config:
        orm_mode = True


@router.get('/')
async def get_all_genre(db: Session = Depends(get_db)):
    return db.query(models.Genre).all()


@router.get('/{id}')
async def get_genre_by_id(id: str, db: Session = Depends(get_db)):
    genre_model = db.query(models.Genre).filter(id == models.Genre.id).first()
    if genre_model is None:
        raise raise_404_exception('Genre')
    return genre_model


@router.post('/')
async def create_genre(genre: Genre, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    genre_model = models.Genre()
    genre_model.name = genre.name
    genre_model.user_id = user.get("id")
    db.add(genre_model)
    db.commit()
    return success_message(201)


@router.put('/{id}')
async def update_genre(id: str, genre: Genre, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    genre_model = db.query(models.Genre).filter(
        user.get("id") == models.Genre.user_id).filter(id == models.Genre.id).first()
    if genre_model is None:
        raise raise_404_exception('Genre')
    genre_model.name = genre.name
    db.add(genre_model)
    db.commit()
    return success_message(200)


@router.delete('/{id}')
async def delete_genre(id: str, genre: Genre, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    genre_model = db.query(models.Genre).filter(
        user.get("id") == models.Genre.user_id).filter(id == models.Genre.id).first()
    if genre_model is None:
        raise raise_404_exception('Genre')
    db.query(models.Genre).filter(user.get(
        "id") == models.Genre.user_id).filter(id == models.Genre.id).delete()
    db.commit()
    return success_message(200)
