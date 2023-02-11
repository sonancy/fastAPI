from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from typing import Optional
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import models
import uuid

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


def raise_404_exception(model):
    return HTTPException(status_code=404, detail=f"{model} not found!", headers={
        'X-Header-Error': f'{model} not found with provided data'})


def success_message(status):
    return {
        'status': status,
        'transaction': 'Successful'
    }


def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_hashed_password(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def verify_user(username: str, password: str, db):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(username, id, expire: Optional[timedelta] = None):
    encode = {"sub": username, "id": id}
    if not expire:
        expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        expire = datetime.utcnow() + expire
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id = uuid.UUID(payload.get("id"))
        if not username or not id:
            return get_user_exception()
        return {"id": id, "username": username}
    except JWTError:
        raise get_user_exception()
