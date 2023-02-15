from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # choose bcrypt as encription tool


def get_password_hash(password):
    return bcrypt_context.hash(password)  # type of encription, in this case by hash


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)
