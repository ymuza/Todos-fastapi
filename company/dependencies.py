from fastapi import Header, HTTPException

"""this file is for dependencies that need to be passed while accessing the 
company apis for security reasons, etc."""


async def get_token_header(internal_token: str = Header(...)):
    """it returns a single header as an example"""
    if internal_token != "allowed":  # allowed will be the secret key in this example
        raise HTTPException(status_code=400, detail="Internal-Token header is invalid")
