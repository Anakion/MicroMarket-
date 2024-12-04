from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.backend.session import get_async_session
from app.models import Product
from app.routers.auth import get_current_user
from app.schemas.product import CreateProduct
from app.services.product import add_new_product_in_db, get_all_products_in_db, product_by_category_in_db, \
    product_detail_in_db, update_product_in_db, delete_product_from_db

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_async_session)],
                       get_user: Annotated[dict, Depends(get_current_user)]):
    all_products_in_db = await get_all_products_in_db(db)
    return all_products_in_db


@router.post('/create')
async def create_product(db: Annotated[AsyncSession, Depends(get_async_session)],
                         get_user: Annotated[dict, Depends(get_current_user)],
                         data: CreateProduct):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        new_product = await add_new_product_in_db(db, data, get_user.get('id'))
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_async_session)],
                              get_user: Annotated[dict, Depends(get_current_user)],
                              category_slug: str):
    category = await product_by_category_in_db(db, category_slug)
    return category


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_async_session)],
                         get_user: Annotated[dict, Depends(get_current_user)],
                         product_slug: str):
    data_product = await product_detail_in_db(db, product_slug)
    return data_product


@router.put('/update/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_async_session)],
                         product_slug: str,
                         get_user: Annotated[dict, Depends(get_current_user)],
                         data: CreateProduct):
    product_update = await db.scalar(select(Product).where(Product.slug == product_slug))
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        if product_update.supplier_id == get_user.get('id') or get_user.get('is_admin'):
            updated_product = await update_product_in_db(db, product_slug, data)
            return updated_product
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to update this product"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method"
        )

@router.delete('/delete')
async def delete_product(db: Annotated[AsyncSession, Depends(get_async_session)],
                         get_user: Annotated[dict, Depends(get_current_user)],
                         product_id: int):
    product_update = await db.scalar(select(Product).where(Product.id == product_id))
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        if product_update.supplier_id == get_user.get('id') or get_user.get('is_admin'):
            delete_product_ = await delete_product_from_db(db, product_id)
            return delete_product_
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to delete this product"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method"
        )