from fastapi import APIRouter, Depends, HTTPException
import uuid
from database import get_db
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from handler import get_current_user, raise_404_exception, success_message, token_exception
import models

router = APIRouter(prefix="/api/bike",
                   tags=["Bike"],
                   responses={404: {"description": "Not found"}})


class Bike(BaseModel):
    name: str = Field(min_length=1)
    model: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    bike_type: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "name": "Name - 1",
                "model": "Model - 1",
                "brand": "Brand - 1",
                "bike_type": "12570c42-cc61-49fb-aa7f-bc08cc55193c"
            }
        }
        orm_mode = True


@router.get('/')
async def get_all_bike(db: Session = Depends(get_db)):
    return db.query(models.Bike).all()


@router.get('/{id}')
async def get_all_bike(id: uuid.UUID, db: Session = Depends(get_db)):
    bike = db.query(models.Bike).filter(models.Bike.id == id).first()
    if not bike:
        raise raise_404_exception('Bike')
    return bike


@router.post("/")
async def create_bike(bike: Bike, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_model = models.Bike()
    bike_model.name = bike.name
    bike_model.bike_type_id = bike.bike_type
    bike_model.brand = bike.brand
    bike_model.model = bike.model
    bike_model.created_by = user.get("id")
    try:
        db.add(bike_model)
        db.commit()
        db.refresh(bike_model)
        return success_message(201)
    except:
        raise HTTPException(
            status_code=409, detail="This bike doesn't exists!")


@router.put('/{id}')
async def get_all_bike(id: uuid.UUID, bike: Bike, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_model = db.query(models.Bike).filter(
        models.Bike.id == id).filter(models.Bike.id == id).first()
    if not bike_model:
        raise raise_404_exception('Bike')
    bike_model.name = bike.name
    bike_model.bike_type_id = bike.bike_type
    bike_model.brand = bike.brand
    bike_model.model = bike.model
    try:
        db.add(bike_model)
        db.commit()
        db.refresh(bike_model)
        return success_message(200)
    except:
        raise HTTPException(
            status_code=409, detail="This bike already exists!")


@router.delete('/{id}')
async def get_all_bike(id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_model = db.query(models.Bike).filter(
        models.Bike.id == id).filter(models.Bike.id == id).first()
    if not bike_model:
        raise raise_404_exception('Bike')
    db.query(models.Bike).filter(models.Bike.id ==
                                 id).filter(models.Bike.id == id).delete()
    db.commit()
    return success_message(200)
