from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.backend.session import get_async_session
from app.schemas.product import CreateProduct
from app.services.product import add_new_product_in_db, get_all_products_in_db, product_by_category_in_db, \
    product_detail_in_db, update_product_in_db

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_async_session)]):
    all_products_in_db = await get_all_products_in_db(db)
    return all_products_in_db


@router.post('/create')
async def create_product(db: Annotated[AsyncSession, Depends(get_async_session)],
                         data: CreateProduct):
    new_product = await add_new_product_in_db(db, data)
    return new_product


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_async_session)],
                              category_slug: str):
    category = await product_by_category_in_db(db, category_slug)
    return category


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_async_session)],
                         product_slug: str):
    data_product = await product_detail_in_db(db, product_slug)
    return data_product


@router.put('/update/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_async_session)],
                         product_slug: str,
                         data: CreateProduct):
    upd_product = await update_product_in_db(db, product_slug, data)
    return upd_product

@router.delete('/delete')
async def delete_product(product_id: int):
    pass