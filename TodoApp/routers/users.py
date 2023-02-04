from .auth import get_user_exception, getCurrentUser, getHashedPassword, authenticate_user
import models
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from .todos import success_message
import sys
sys.path.append("..")

router = APIRouter(
    prefix='/users',
    tags=["Users"],
    responses={404: {"description": "User not found!"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@router.get("/")
def getAllUsers(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id is None:
        user = db.query(models.Users).all()
    else:
        user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.get("/{id}")
def getUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.post('/change-password')
def changePassword(currentPassword: str = Form(), newPassword: str = Form(), user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    isAuthenticated = authenticate_user(username=user.get(
        "username"), password=currentPassword, db=db)
    if not isAuthenticated:
        raise get_user_exception()
    newPassword = getHashedPassword(newPassword)
    user_model = db.query(models.Users).filter(
        user.get("id") == models.Users.id).first()
    user_model.hashed_password = newPassword
    db.add(user_model)
    db.commit()
    return success_message(200)


@router.delete('/{id}')
def deleteUser(user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception
    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()
    return success_message(200)
