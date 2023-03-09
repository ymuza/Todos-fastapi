import sys
sys.path.append("..")  # allows to import everything in todos parent directory
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from .auth import get_current_user, get_user_exception

router = APIRouter(prefix="/address",
                   tags=["address"],
                   responses={404: {"description": "not found"}}
                   )

# models.Base.metadata.create_all(bind=engine) , not needed as with alembic we
# already created the new table and columns


def get_db():
    """connects to the db"""
    data_base = None
    try:
        data_base = SessionLocal()
        yield data_base
    finally:
        data_base.close()


class Address(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postalcode: str
    apartment_number: Optional[int]


@router.post("/")
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         data_base: Session = Depends(get_db)):
    """creates the user address"""
    if user is None:
        raise get_user_exception()
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    address_model.apartment_number = address.apartment_number

    data_base.add(address_model)

    data_base.flush()  # is like a commit, but it returns the id or column created

    user_model = data_base.query(models.Users).filter(models.Users.id == user.get("id")).first()

    user_model.address_id = address_model.id

    data_base.add(user_model)

    data_base.commit()
