from fastapi import APIRouter, Depends, Form
from handlers import success_message, get_hashed_password, get_current_user, get_user_exception, verify_user
import models
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"detail": "User not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


class User(BaseModel):
    email: Optional[str]
    username: str
    first_name: str
    last_name: str
    hashed_password: str

    class Config:
        orm_mode = True


@router.post('/create-user')
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name

    hashed_password = get_hashed_password(user.hashed_password)

    user_model.hashed_password = hashed_password
    db.add(user_model)
    db.commit()
    return success_message(201)


@router.put('/change-password')
def change_password(current_password: str = Form(), new_password: str = Form(), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user = verify_user(username=user.get("username"),
                       password=current_password, db=db)
    if not user:
        raise get_user_exception()
    user.hashed_password = get_hashed_password(new_password)
    db.add(user)
    db.commit()
    return success_message(200)


@router.put('/update-user')
def update_user(user: dict = Depends(get_current_user), email: str = Form(), first_name: str = Form(), last_name: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user = verify_user(username=user.get("username"),
                       password=password, db=db)
    if not user:
        raise get_user_exception()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    db.add(user)
    db.commit()
    return success_message(200)


@router.delete('/delete-user')
def delete_user(password: str = Form(), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user = verify_user(username=user.get("username"),
                       password=password, db=db)
    if not user:
        raise get_user_exception()
    user.is_active = False
    db.add(user)
    db.commit()
    return success_message(200)
