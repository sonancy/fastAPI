from fastapi import APIRouter, Depends, HTTPException
import uuid
from database import get_db
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from handler import get_current_user, raise_404_exception, success_message, token_exception
import models

router = APIRouter(prefix="/api/bike/bike-type",
                   tags=["Bike"],
                   responses={404: {"description": "Not found"}})


class BikeType(BaseModel):
    name: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "name": "Name - 1"
            }
        }
        orm_mode = True


@router.get('/')
async def get_all_bike_type(db: Session = Depends(get_db)):
    return db.query(models.BikeType).all()


@router.get('/{id}')
async def get_bike_type(id: uuid.UUID, db: Session = Depends(get_db)):
    bike_type = db.query(models.BikeType).filter(
        models.BikeType.id == id).first()
    if not bike_type:
        raise raise_404_exception('Bike Type')
    return bike_type


@router.post("/")
async def create_bike_type(bikeType: BikeType, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_type_model = models.BikeType()
    bike_type_model.name = bikeType.name
    bike_type_model.created_by = user.get("id")
    try:
        db.add(bike_type_model)
        db.commit()
        db.refresh(bike_type_model)
        return success_message(201)
    except:
        raise HTTPException(
            status_code=409, detail="This bike type already exists!")


@router.put('/{id}')
async def update_bike_type(id: uuid.UUID, bikeType: BikeType, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_type = db.query(models.BikeType).filter(models.BikeType.id == id).filter(
        models.BikeType.created_by == user.get("id")).first()
    if not bike_type:
        raise raise_404_exception('Bike Type')
    bike_type.name = bikeType.name
    try:
        db.add(bike_type)
        db.commit()
        db.refresh(bike_type)
        return success_message(200)
    except:
        raise HTTPException(
            status_code=409, detail="This bike type already exists!")


@router.delete('/{id}')
async def delete_bike_type(id: uuid.UUID, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    bike_type = db.query(models.BikeType).filter(models.BikeType.id == id).filter(
        models.BikeType.created_by == user.get("id")).first()
    if not bike_type:
        raise raise_404_exception('Bike Type')
    db.query(models.BikeType).filter(models.BikeType.id == id).filter(
        models.BikeType.created_by == user.get("id")).delete()
    db.commit()
    return success_message(200)
