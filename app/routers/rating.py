from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.session import get_async_session
from app.models import Product
from app.models.feedback import FeedBack
from app.models.rating import Rating
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.rating import ReviewRequest

router = APIRouter(prefix='/rating', tags=['rating'])

@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_async_session)]):
    feedbacks = await db.execute(select(FeedBack).where(FeedBack.is_active == True))
    feedbacks_list = feedbacks.scalars().all()

    ratings = await db.execute(select(Rating).where(Rating.is_active == True))
    ratings_list = ratings.scalars().all()

    return {
        'feedbacks': feedbacks_list,
        'ratings': ratings_list
    }

@router.get('/products_reviews/{product_id}')
async def product_reviews(db: Annotated[AsyncSession, Depends(get_async_session)], product_id: int):
    feedbacks = await db.execute(
        select(FeedBack).where(FeedBack.product_id == product_id, FeedBack.is_active == True)
    )
    ratings = await db.execute(
        select(Rating).where(Rating.product_id == product_id, Rating.is_active == True)
    )
    return {
        "feedbacks": feedbacks.scalars().all(),
        "ratings": ratings.scalars().all()
    }


@router.post('/add_review')
async def add_review(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        review_request: ReviewRequest,
        current_user: User = Depends(get_current_user)
):

    # Get product by ID
    result = await db.execute(select(Product).filter(Product.id == review_request.product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")

    # Create new (FeedBack)
    feedback = FeedBack(
        user_id=current_user['id'],
        product_id=review_request.product_id,
        rating_id=None,
        comment=review_request.comment,
        is_active = True
    )
    db.add(feedback)
    await db.commit()

    # create new (Rating)
    rating = Rating(
        user_id=current_user['id'],
        product_id=review_request.product_id,
        grade=review_request.rating,
        is_active=True
    )
    db.add(rating)
    await db.commit()

    # Linking the review to the rating
    feedback.rating_id = rating.id  # Привязываем rating_id в FeedBack
    db.add(feedback)
    await db.commit()

    # Recalculating the average rating of an item
    result_ratings = await db.execute(
        select(Rating).filter(Rating.product_id == review_request.product_id, Rating.is_active == True))
    ratings = result_ratings.scalars().all()

    if ratings:
        avg_rating = sum(r.grade for r in ratings) / len(ratings)
        product.rating = avg_rating
        await db.commit()

    return {"message": "Review and rating added successfully"}
