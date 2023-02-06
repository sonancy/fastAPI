from fastapi import FastAPI
from routers import auth, anime, genre, user
from database import engine
import models

app = FastAPI()

app.include_router(anime.router)

app.include_router(auth.router)

app.include_router(genre.router)

app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)
