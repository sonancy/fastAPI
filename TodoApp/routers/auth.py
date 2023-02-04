import models
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional
from passlib.context import CryptContext
from database import engine, SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import sys
sys.path.append("..")

SECRET_KEY = 'nancysolanki#007'
ALGORITHM = "HS256"


class User(BaseModel):
    username: str
    email: Optional[str]
    password: str
    first_name: str
    last_name: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not authorize!"}}
)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@router.post('/create-user')
def createUser(user: User, db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.email = user.email
    user_model.username = user.username
    user_model.is_active = True

    hashed_password = getHashedPassword(user.password)

    user_model.hashed_password = hashed_password

    db.add(user_model)
    db.commit()

    return {
        "status": 404,
        "transaction": "Successful"
    }


@router.post('/token')
async def getToken(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    return {"Token": createAccessToken(user.username, user.id, timedelta(minutes=20))}


def getHashedPassword(password):
    return bcrypt_context.hash(password)


def getCurrentUser(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if not username or not id:
            raise get_user_exception()
        return {"username": username, "id": id}
    except JWTError:
        raise get_user_exception()


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(
        username == models.Users.username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def createAccessToken(username: str, id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
