from fastapi import APIRouter, Depends
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from typing import Optional
from handlers import raise_404_exception, success_message
from handlers import get_current_user, get_user_exception
import models

router = APIRouter(
    prefix='/anime',
    tags=["Anime"],
    responses={404: {"detail": "Anime not found!"}}
)

router.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


class Anime(BaseModel):
    title: str
    episodes: int = Field(default=1)
    status: str = Field(default="Ongoing")
    duration: str = Field(default="24 min per episode")
    ratings: float = Field(ge=0, le=10)
    # photo = ImageField(upload_to='anime')
    genre_id: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                'title': 'Attack on Titan',
                'episodes': 87,
                'status': 'Ongoing / Finished',
                'duration': '24 min per episode',
                'ratings': 9.9,
                # photo = ImageField(upload_to='anime')
                'description': 'Optional'
            }
        }
        orm_mode = True


@router.get("/")
async def get_all_anime(search: Optional[str] = '', db: Session = Depends(get_db)):
    return db.query(models.Anime).filter(models.Anime.title.contains(search)).all()


@router.get("/{id}")
async def get_anime_by_id(id: str, db: Session = Depends(get_db)):
    anime_model = db.query(models.Anime).filter(models.Anime.id == id).first()
    if anime_model is None:
        raise raise_404_exception('Anime')
    return anime_model


@router.post("/")
async def create_anime(anime: Anime, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    anime_model = models.Anime()
    anime_model.title = anime.title
    anime_model.episodes = anime.episodes
    anime_model.status = anime.status
    anime_model.description = anime.description
    anime_model.duration = anime.duration
    anime_model.ratings = anime.ratings
    anime_model.genre_id = anime.genre_id
    anime_model.user_id = user.get("id")
    db.add(anime_model)
    db.commit()
    return success_message(201)


@router.put("/{id}")
async def update_anime(id: str, anime: Anime, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    anime_model = db.query(models.Anime).filter(models.Anime.id == id).filter(
        models.Anime.user_id == user.get("id")).first()
    if anime_model is None:
        raise raise_404_exception('Anime')
    anime_model.title = anime.title
    anime_model.episodes = anime.episodes
    anime_model.status = anime.status
    anime_model.description = anime.description
    anime_model.duration = anime.duration
    anime_model.ratings = anime.ratings
    anime_model.genre_id = anime.genre_id
    db.add(anime_model)
    db.commit()
    return success_message(200)


@router.delete("/{id}")
async def delete_anime(id: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    anime_model = db.query(models.Anime).filter(
        models.Anime.user_id == user.get("id")).filter(models.Anime.id == id).first()
    if anime_model is None:
        raise raise_404_exception('Anime')
    db.query(models.Anime).filter(models.Anime.user_id ==
                                  user.get("id")).filter(models.Anime.id == id).delete()
    db.commit()
    return success_message(200)
