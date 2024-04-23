from datetime import datetime, timedelta

import prisma
import prisma.models
from fastapi.exceptions import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED


class LoginResponse(BaseModel):
    """
    Response model for the login request containing the JWT token for authentication.
    """

    access_token: str
    expires_in: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    """
    Verifies a password against its hashed version.

    :param plain_password: Password in plain text to verify.
    :param hashed_password: The hashed version of the password to verify against.

    :return: `True` if the password is correct, otherwise `False`.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT token that stores the user data, with an expiry.

    :param data: Data to encode in the token.
    :param expires_delta: The lifetime of the token.

    :return: The JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login(username: str, password: str) -> LoginResponse:
    """
    Authenticates users and returns a JWT token.

    :param username: The user's unique username.
    :param password: The user's password.

    :return: Response model for the login request containing the JWT token for authentication.

    :raises HTTPException: If authentication fails.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponse(
        access_token=access_token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
    )
