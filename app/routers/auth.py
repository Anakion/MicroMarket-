from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.config import settings
from app.backend.security import verify_password, verify_token
from app.backend.session import get_async_session
from app.models.user import User
from app.schemas.auth import CreateUser
from app.services.auth import create_user_in_db

router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def create_access_token(username: str, user_id: int, is_admin: bool, is_supplier: bool, is_customer: bool,
                              expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin, 'is_supplier': is_supplier,
              'is_customer': is_customer}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = verify_token(token)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_admin: str = payload.get('is_admin')
        is_supplier: str = payload.get('is_supplier')
        is_customer: str = payload.get('is_customer')
        expire = payload.get('exp')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user'
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )

        return {
            'username': username,
            'id': user_id,
            'is_admin': is_admin,
            'is_supplier': is_supplier,
            'is_customer': is_customer,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )

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
    token = await create_access_token(user.username, user.id, user.is_admin, user.is_supplier, user.is_customer,
                                      expires_delta=timedelta(minutes=5))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

# @router.get('/read_current_user')
# async def read_current_user(user: User = Depends(oauth2_scheme)):
#     return user


@router.get('/read_current_user')
async def read_current_user(user: User = Depends(get_current_user)):
    return {'User': user}


