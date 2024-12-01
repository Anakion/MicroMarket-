from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.security import verify_password
from app.backend.session import get_async_session
from app.models.user import User
from app.schemas.auth import CreateUser
from app.services.auth import create_user_in_db

router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post('/')
async def create_user(db: Annotated[AsyncSession, Depends(get_async_session)], new_user: CreateUser):
    result = await create_user_in_db(db, new_user)
    return result


async def authenticate_user(db: Annotated[AsyncSession, Depends(get_async_session)], username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not verify_password(password, user.hashed_password) or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post('/token')
async def login(db: Annotated[AsyncSession, Depends(get_async_session)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )

    return {
        'access_token': user.username,
        'token_type': 'bearer'
    }

@router.get('/read_current_user')
async def read_current_user(user: User = Depends(oauth2_scheme)):
    return user