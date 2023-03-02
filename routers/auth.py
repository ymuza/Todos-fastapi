import sys
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models

sys.path.append("..")  # this will allow to import everything in auth's parent directory
from database import SessionLocal, engine
from exceptions import get_user_exception, token_exception
from password_management import get_password_hash, verify_password

SECRET_KEY = ""
ALGORITHM = "HS256"



class CreateUser(BaseModel):
    """User table data"""

    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


# creates the db and does all the importan stuff for the table
models.Base.metadata.create_all(bind=engine)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str, data_base):
    """authenticates user"""
    user = (
        data_base.query(models.Users).filter(models.Users.username == username).first()
    )

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


router = APIRouter(
    prefix="/Auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)
# instead of starting auth as an app,I extend the capability to main.
# prefix, tags and responses are a way of organizing the api.


def get_db():
    """retrieves the conection to the db"""
    data_base = None
    try:
        data_base = SessionLocal()
        yield data_base
    finally:
        data_base.close()


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    """creates the access token for the user"""
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    """gets current user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise get_user_exception() from exc


@router.post(
    "/create/user"
)  # change app for router to extend the capability to main file
async def create_new_user(
    create_user: CreateUser, data_base: Session = Depends(get_db)
):
    """creates a new user in the db"""
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.firstname = create_user.first_name
    create_user_model.lastname = create_user.last_name

    hash_password = get_password_hash(
        create_user.password
    )  # proceed to hash user password

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True

    data_base.add(create_user_model)
    data_base.commit()

    return {"user has been added."}


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    data_base: Session = Depends(get_db),
):
    """returns the access token for the user"""
    user = authenticate_user(form_data.username, form_data.password, data_base)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {"token": token}
