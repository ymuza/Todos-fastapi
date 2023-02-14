from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from exceptions import http_exception
from responses import successful_response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creates the database (tables & columns)


def get_db():
    db = None
    try:
        db = SessionLocal()  # starts the db session
        yield db
    finally:
        db.close()  # close the db session regardless of the use


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="the priority must be between 1-5")
    complete: bool


# Depends() is a way to declare things that are required for the app/function to work by injecting the dependencies
@app.get("/")
async def read_all(db: Session = Depends(get_db)):  # as session depends on get_db, we are sure to close the connection
    return db.query(models.Todos).all()  # returns all the records from the Todos


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()  # first() returns the value and stops going through the db
    if todo_model is not None:
        return todo_model
    else:
        raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)  # places an object in the session
    db.commit()  # flushes changes and COMMITS () the change

    return successful_response(200)


@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)


@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise http_exception()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return successful_response(200)
