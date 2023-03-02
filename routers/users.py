import sys

sys.path.append("..")

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine
from password_management import verify_password
from .auth import get_current_user, get_password_hash, get_user_exception

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    """db connection"""
    data_base = None
    try:
        data_base = SessionLocal()
        yield data_base
    finally:
        data_base.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/")
async def read_all(data_base: Session = Depends(get_db)):
    """retrieves all the users"""
    return data_base.query(models.Users).all()


@router.get("/user/{user_id}")
async def get_user_by_path(user_id: int, data_base: Session = Depends(get_db)):
    """retrieves an user by user_id"""
    user_model = (
        data_base.query(models.Users).filter(models.Users.id == user_id).first()
    )
    if user_model is not None:
        return user_model
    return "Invalid user id"


@router.get("/user")
async def get_user_by_query(user_id: int, data_base: Session = Depends(get_db)):
    """retrieves a user by query"""
    user_model = (
        data_base.query(models.Users).filter(models.Users.id == user_id).first()
    )
    if user_model is not None:
        return user_model
    return "Invalid user id"


@router.put("/user/password")
async def user_password_change(
    user_verification: UserVerification,
    user: dict = Depends(get_current_user),
    data_base: Session = Depends(get_db),
):
    """changes user password"""
    if user is None:
        raise get_user_exception()
    user_model = (
        data_base.query(models.Users).filter(models.Users.id == user.get("id")).first()
    )

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(
            user_verification.password, user_model.hashed_password
        ):
            user_model.hashed_password = get_password_hash(
                user_verification.new_password
            )
            data_base.add(user_model)
            data_base.commit()
            return "Successful"
        return "invalid user or request"


@router.delete("/user")
async def delete_user(user: dict = Depends(get_current_user), data_base : Session = Depends(get_db)):
    """deletes user"""
    if user is None:
        raise get_user_exception()

    user_model = data_base.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        return "Invalid user or request"

    data_base.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    data_base.commit()
    return 'Deletion successful'
