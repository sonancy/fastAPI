import models
from handler import get_hashed_password, success_message, verify_user, get_current_user, token_exception
from sqlalchemy.orm import Session
from database import get_db, engine
from pydantic import BaseModel, root_validator, Field
from fastapi import APIRouter, Depends, HTTPException, Form, status

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    responses={404: {"description": "Not found"}}
)


class User(BaseModel):
    username: str = Field(min_length=1)
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    confirm_password: str = Field(min_length=1)
    password: str = Field(min_length=1)

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        return values


class UpdateUser(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)


@router.post('/create-user')
async def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(user.password)
    user_model = models.User()
    user_model.name = user.name
    user_model.password = hashed_password
    user_model.email = user.email
    user_model.username = user.username

    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return success_message(201)
    except:
        raise HTTPException(
            status_code=409, detail="This user already exists!")


@router.post('/change-password')
async def change_password(old_password=Form(), new_password=Form(), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    user = verify_user(user.get("username"), old_password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password")
    user.password = get_hashed_password(new_password)
    db.add(user)
    db.commit()
    return success_message(200)


@router.put('/update-user')
async def update_user(newData: UpdateUser, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    user_model = db.query(models.User).filter(
        models.User.id == user.get("id")).first()
    user_model.name = newData.name
    user_model.email = newData.email
    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return success_message(200)
    except:
        raise HTTPException(
            status_code=409, detail="This email already exists!")


@router.delete('/delete-user')
async def delete_user(password=Form(), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise token_exception()
    user = verify_user(user.get("username"), password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password")
    db.query(models.User).filter(
        models.User.id == user.id).delete()
    db.commit()
    return success_message(200)
