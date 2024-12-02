from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from app.backend.config import settings

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto")

def get_password_hash(password: str) -> str:
    """
        Hashes the password using bcrypt.

        :param password: Password
        :return: Hashed password
    """
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Verifies the password using bcrypt.

        :param plain_password: Password
        :param hashed_password: Hashed password
        :return: True if the password is correct, False otherwise
    """
    return bcrypt_context.verify(plain_password, hashed_password)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired"
        )