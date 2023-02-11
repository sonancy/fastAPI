from handler import verify_user, token_exception, create_token
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)


@router.post("/get-token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = verify_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    return {"Token": create_token(user.username, str(user.id), expire=timedelta(minutes=20))}
