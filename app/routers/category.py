from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.backend.session import get_async_session
from app.schemas.category import CreateCategory
from app.services.category import create_category_db, get_all_categories_in_db, delete_category_in_db

router = APIRouter(prefix='/category', tags=['category'])


@router.get("/all_categories")
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_async_session)]):
    all_category = await get_all_categories_in_db(db)
    return all_category


@router.post('/create')
async def create_category(db: Annotated[AsyncSession, Depends(get_async_session)], category: CreateCategory):
    new_category = await create_category_db(db, category)
    return JSONResponse(
        content={'Category': f'new category {category.name} success'},
        status_code=201
    )


@router.put('/update_category')
async def update_category():
    pass


@router.delete('/delete')
async def delete_category(db: Annotated[AsyncSession, Depends(get_async_session)], category_id: int):
    return await delete_category_in_db(db, category_id)
