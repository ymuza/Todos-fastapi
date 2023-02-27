from typing import Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from auth import get_current_user, get_user_exception
from database import SessionLocal, engine
from exceptions import http_exception
from responses import successful_response

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creates the database (tables & columns)


def get_db():
    """conects to the db"""
    data_base = None
    try:
        data_base = SessionLocal()  # starts the data_base session
        yield data_base
    finally:
        data_base.close()  # close the data_base session regardless of the use


class Todo(BaseModel):
    """todos table data"""

    title: str
    description: Optional[str]
    complete: bool
    priority: int = Field(gt=0, lt=6, description="the priority must be between 1-5")


# "Depends()" is a way to declare things that are required for the app/function
# to work by injecting the dependencies
@app.get("/")
async def read_all(
    data_base: Session = Depends(get_db),
):  # as session depends on get_data_base, we are sure to close the connection
    """gets all the records"""
    return data_base.query(models.Todos).all()  # returns all the records from the Todos


@app.get("/todos/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), data_base: Session = Depends(get_db)
):
    """gets every Todos of a particular user"""
    if user is None:
        raise get_user_exception()
    return (
        data_base.query(models.Todos)
        .filter(models.Todos.owner_id == user.get("id"))
        .all()
    )


@app.get("/todo/{todo_id}")
async def read_todo(
    todo_id: int,
    user: dict = Depends(get_current_user),
    data_base: Session = Depends(get_db),
):
    """gets a "to do" activity by passing a todo_id"""
    if user is not None:
        raise get_user_exception()
    todo_model = (
        data_base.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )  # first() returns the value and stops going through the data_base

    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user),
                      data_base: Session = Depends(get_db)):
    """create a "to do" activity"""
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    data_base.add(todo_model)  # places an object in the session
    data_base.commit()  # flushes changes and COMMITS () the change

    return successful_response(200)


@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user),
                      data_base: Session = Depends(get_db)):
    """updates the todos. it takes a user jwt,
    finds the id where the user id matches the owner id """
    if user is None:
        raise get_user_exception()

    todo_model = (data_base.query(models.Todos)
                  .filter(models.Todos.id == todo_id)
                  .filter(models.Todos.owner_id == user.get("id"))
                  .first())

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    data_base.add(todo_model)
    data_base.commit()

    return successful_response(200)


@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user),
                      data_base: Session = Depends(get_db)):
    """deletes a "to do" activity by passing a todo_id"""
    if user is None:
        raise get_user_exception()
    todo_model = (
        data_base.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise http_exception()

    data_base.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    data_base.commit()

    return successful_response(200)
