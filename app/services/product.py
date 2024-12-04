from fastapi import HTTPException
from slugify import slugify
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status
from sqlalchemy import or_

from app.models import Product, Category
from app.schemas.product import CreateProduct


async def add_new_product_in_db(db: AsyncSession, data: CreateProduct, supplier_id: int):
    await db.execute(insert(Product).values(
        name=data.name,
        slug=slugify(data.name),
        description=data.description,
        price=data.price,
        image_url=data.image_url,
        stock=data.stock,
        rating=data.rating,
        supplier_id=supplier_id,
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


async def product_by_category_in_db(db: AsyncSession, category_slug_db: str):
    category = await db.scalar(select(Category).where(Category.name == category_slug_db))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id))
    all_category_ids = [category.id] + [subcat.id for subcat in subcategories]
    products = await db.scalars(
        select(Product).where(
            Product.category_id.in_(all_category_ids),
            Product.is_active == True,
            Product.stock > 0
        )
    )

    return products.all()


async def product_detail_in_db(db: AsyncSession, product_slug: str):
    get_detail_product = await db.scalar(
        select(Product).where(
            or_(
                Product.name == product_slug,
                Product.slug == product_slug
            )
        )
    )
    if get_detail_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no product")
    return get_detail_product


async def update_product_in_db(db: AsyncSession, product_slug: str, data: CreateProduct):
    get_product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if get_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found")


    get_product.name = data.name
    get_product.description = data.description
    get_product.price = data.price

    db.add(get_product)
    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Product update is successful"
    }


async def delete_product_from_db(db: AsyncSession, product_id: int):
    get_product = await db.scalar(select(Product).where(Product.id == product_id))
    if get_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found")

    await db.execute(update(Product).where(Product.id == product_id).values(is_active=False))
    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Product delete is successful"
    }
