from fastapi import HTTPException
from slugify import slugify
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.models import Product
from app.schemas.product import CreateProduct


async def add_new_product_in_db(db: AsyncSession, data: CreateProduct):
    await db.execute(insert(Product).values(
        name=data.name,
        slug=slugify(data.name),
        description=data.description,
        price=data.price,
        image_url=data.image_url,
        stock=data.stock,
        rating=data.rating,
        category_id=data.category
    ))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful add new product'
    }


async def get_all_products_in_db(db: AsyncSession):
    result = await db.execute(select(Product).where(Product.is_active == True, Product.stock > 0))

    all_products = result.scalars().all()

    if not all_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no products'
        )

    return all_products
