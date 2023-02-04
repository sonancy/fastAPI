from fastapi import FastAPI
from database import engine
from routers import auth, todos, users
import models

app = FastAPI()

app.include_router(auth.router)

app.include_router(todos.router)

app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)
