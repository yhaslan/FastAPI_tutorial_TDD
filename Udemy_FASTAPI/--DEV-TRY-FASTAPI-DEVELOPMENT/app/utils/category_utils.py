from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category_schema import CategoryCreate


def check_existing_category(db: Session, category_data: CategoryCreate):
    existing_category = (
        db.query(Category)
        .filter(  # filter method in sql alchemy allows us to filter only rows that meet certain criteria
            (Category.slug == category_data.slug)
            | (Category.name == category_data.name)
            & (Category.level == category_data.level)
        )
        .first()  # we need to make sure there is at least one but it doesnt matter many dedi
        # nasil many olcak ki zaten tum olay bunlarin unique olmaqsi degil mi
    )

    # so above we made a query with filter, thats gonna return either a single object or nothing

    if existing_category:
        if (
            existing_category.name == category_data.name
            and existing_category.level == category_data.level
        ):
            detail_msg = "Category name and level already exists"
        else:
            detail_msg = "Category slug already exists"

        raise HTTPException(status_code=400, detail=detail_msg)
