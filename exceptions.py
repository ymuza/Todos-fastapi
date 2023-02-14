from fastapi import HTTPException


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")


def user_validation_exception():
    return HTTPException(status_code=404, detail="User not found")
