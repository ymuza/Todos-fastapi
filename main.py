from fastapi import Depends, FastAPI

import models
from company import company_apis, dependencies
from database import engine
from routers import auth, todos, users, address

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creates the database (tables & columns)

app.include_router(auth.router)  # includes the auth file
app.include_router(todos.router)  # includes the todos file
app.include_router(users.router)
app.include_router(address.router)
app.include_router(
    company_apis.router,
    prefix="/company_apis",
    tags=["company_apis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "internal use only"}},
)
# company_apis are separated from auth and todos as they are for internal use.
# the parameter 'dependencies' is to recieve for example a security dependency.

