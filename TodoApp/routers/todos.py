from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from typing import Optional
from .auth import get_user_exception, getCurrentUser
import sys
sys.path.append("..")
router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found!"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0,  lt=6, description="The priority must be between 1-5")
    complete: bool


# router.get('/')
# async def getAllTodos(db: Session = Depends(get_db)):
#     return db.query(models.Todos).all()


# router.get('/{id}')
# async def getTodoById(id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todos).filter(models.Todos.id == id).first()
#     if todo is None:
#         raise raise_404_exception()
#     else:
#         return todo


# router.post('/')
# def createTodo(todo: Todo, db: Session = Depends(get_db)):
#     todo_model = models.Todos()
#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.complete = todo.complete
#     todo_model.priority = todo.priority
#     todo_model.user = todo.user

#     db.add(todo_model)
#     db.commit()

#     return success_message(200)


# router.put('/{id}')
# def updateTodo(id: int, todo: Todo, db: Session = Depends(get_db)):
#     todo_model = db.query(models.Todos).filter(models.Todos.id == id).first()

#     if todo_model is None:
#         raise raise_404_exception()

#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.complete = todo.complete
#     todo_model.priority = todo.priority

#     db.add(todo_model)
#     db.commit()

#     return success_message(200)


# router.delete('/{id}')
# def deleteTodo(id: int, db: Session = Depends(get_db)):
#     todo_model = db.query(models.Todos).filter(models.Todos.id == id).first()

#     if todo_model is None:
#         raise raise_404_exception()

#     db.query(models.Todos).filter(models.Todos.id == id).delete()

#     db.commit()

#     return success_message(200)

@router.get('/')
async def getTodoByUser(user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(user.get("id") == models.Todos.user_id).all()


@router.get('/{id}')
async def getTodoByUserAndId(id: int, user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo = db.query(models.Todos).filter(
        user.get("id") == models.Todos.user_id).filter(models.Todos.id == id).first()
    if todo is None:
        raise raise_404_exception()
    else:
        return todo


@router.post('/')
async def createTodo(todo: Todo, user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.complete = todo.complete
    todo_model.priority = todo.priority
    todo_model.user_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return success_message(200)


@router.put('/{id}')
async def updateTodo(todo: Todo, id: int, user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == id).filter(models.Todos.user_id == user.get("id")).first()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.complete = todo.complete
    todo_model.priority = todo.priority

    db.add(todo_model)
    db.commit()

    return success_message(200)


@router.delete('/{id}')
async def updateTodo(id: int, user: dict = Depends(getCurrentUser), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    db.query(models.Todos).filter(models.Todos.id == id).filter(
        models.Todos.user_id == user.get("id")).delete()

    db.commit()

    return success_message(200)


def raise_404_exception():
    return HTTPException(status_code=404, detail="Todo not found!")


def success_message(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }
