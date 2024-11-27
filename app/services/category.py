from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy import insert, update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas.category import CreateCategory


async def create_category_db(db: AsyncSession, new_category: CreateCategory):
    await db.execute(insert(Category).values(
        name=new_category.name,
        parent_id=new_category.parent_id,
        slug=slugify(new_category.name)
    ))
    await db.commit()
    return {
        'status_code': 201,
        'transaction': 'Successful'
    }


async def get_all_categories_in_db(db: AsyncSession):
    result = await db.execute(select(Category).where(Category.is_active == True))
    return result.scalars().all()


async def delete_category_in_db(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id,
                                                     Category.is_active == True))
    category = result.scalars().first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )


    await db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category deletion successful'
    }