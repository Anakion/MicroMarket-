from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.security import get_password_hash
from app.models.user import User
from app.schemas.auth import CreateUser
from starlette import status


async def create_user_in_db(db: AsyncSession, new_user: CreateUser):
    await db.execute(insert(User).values(first_name=new_user.first_name,
                                         last_name=new_user.last_name,
                                         username=new_user.username,
                                         email=new_user.email,
                                         hashed_password=get_password_hash(new_user.password),
                                         ))
    await db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


