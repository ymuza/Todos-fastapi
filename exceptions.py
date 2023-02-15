from fastapi import HTTPException, status


def http_exception():
    """404 exception when todo' is not found"""
    return HTTPException(status_code=404, detail="Todo not found")


def user_validation_exception():
    """404 exception when user is not found"""
    return HTTPException(status_code=404, detail="User not found")


def get_user_exception():
    """for when user can't validate the credentials"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    """user password or username is incorrect"""
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
