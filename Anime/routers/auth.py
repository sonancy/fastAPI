from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import timedelta
from handlers import token_exception, verify_user, create_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"detail": "Not authorized"}}
)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@router.post('/token')
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = verify_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    return {"Token": create_token(user.username, user.id, expire=timedelta(minutes=20))}
