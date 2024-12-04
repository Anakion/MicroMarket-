from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette import status
from app.backend.session import get_async_session
from app.routers.auth import get_current_user
from app.schemas.category import CreateCategory
from app.services.category import create_category_db, get_all_categories_in_db, delete_category_in_db, \
    update_category_in_db

router = APIRouter(prefix='/category', tags=['category'])


@router.get("/all_categories")
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_async_session)]):
    all_category = await get_all_categories_in_db(db)
    return all_category


@router.post('/create')
async def create_category(db: Annotated[AsyncSession, Depends(get_async_session)], category: CreateCategory,
                          get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        new_category = await create_category_db(db, category)
        return JSONResponse(
            content={'Category': f'new category {category.name} success'},
            status_code=status.HTTP_201_CREATED
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be admin user for this'
        )


@router.put('/update_category')
async def update_category(db: Annotated[AsyncSession, Depends(get_async_session)],
                          get_user: Annotated[dict, Depends(get_current_user)],
                          category_id: int,
                          update_category_db: CreateCategory):
    if category_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    if get_user.get('is_admin'):
        update_categories = await update_category_in_db(db, category_id, update_category_db)
        return update_categories
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be admin user for this'
        )



@router.delete('/delete')
async def delete_category(db: Annotated[AsyncSession, Depends(get_async_session)],
                          get_user: Annotated[dict, Depends(get_current_user)],
                          category_id: int):
    if get_user.get('is_admin'):
        _delete_category = await delete_category_in_db(db, category_id)
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Category delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be admin user for this'
        )