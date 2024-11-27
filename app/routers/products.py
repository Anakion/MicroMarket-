from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.session import get_async_session
from app.schemas.product import CreateProduct
from app.services.product import add_new_product_in_db, get_all_products_in_db

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
async def product_by_category(category_slug: str):
    pass


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str):
    pass


@router.put('/detail/{product_slug}')
async def update_product(product_slug: str):
    pass


@router.delete('/delete')
async def delete_product(product_id: int):
    pass