from fastapi import FastAPI
from routers import bike, auth, user, bike_type, like, comment
from database import engine
import models

app = FastAPI()

app.include_router(bike.router)

app.include_router(auth.router)

app.include_router(user.router)

app.include_router(bike_type.router)

app.include_router(like.router)

app.include_router(comment.router)

models.Base.metadata.create_all(bind=engine)
