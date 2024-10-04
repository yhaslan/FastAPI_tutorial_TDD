import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connetion import SessionLocal, get_db_session
from app.models import Category
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryDeleteReturn,
    CategoryReturn,
    CategoryUpdate,
)
from app.utils.category_utils import check_existing_category

router = APIRouter()
db = SessionLocal()
logger = logging.getLogger(__name__)


# Endpoint to retrieve all categories
@router.get("/", response_model=List[CategoryReturn])
def get_categories(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        logger.error(f"Unexpected error while retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoint to retrieve a category by its slug
@router.get("/slug/{category_slug}", response_model=CategoryReturn)
def get_category_by_slug(category_slug: str, db: Session = Depends(get_db_session)):
    try:
        category = (
            db.query(Category).filter(Category.slug == category_slug).first()
        )  # filter
        if not category:
            raise HTTPException(status_code=404, detail="Category does not exist")
        return category
    except HTTPException:  # bu hangi tip icin
        raise
    except Exception as e:
        logger.error(f"Unexpected error while retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/", response_model=CategoryReturn, status_code=201
)  # response_model the class we made
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db_session)
):
    try:
        check_existing_category(db, category_data)  # IMPORTED
        """ dikkat et bunu try in icine koymamamk onemli cunku biz buna 400 error vermesini soyledik
            ama try'in icine koyarsak direkt except e gecip bize 500 error vercek
            """
        # Depends here ensures each handler receives its own db session ???
        # like each request has its own isolated db session to avoid conflicts
        new_category = Category(**category_data.model_dump())
        # model_dump is one method of pydantic basemodel, see: https://docs.pydantic.dev/latest/api/base_model/
        # which we inherited when creating the CategoryCreate class
        # The model_dump method you've provided is a custom method added to
        # Pydantic's BaseModel or a subclass of it. This method is used for
        # serializing the model instance into a dictionary representation.
        db.add(new_category)
        db.commit()  # bcz we hadn't chosen autocommit
        db.refresh(new_category)  # this is used to refresh the object state from the
        # corresponding db row. when receive an object from a db, sql alchemy keeps
        # track of its state n attributes
        # however oif changes are made to an underlying row in the db by another
        # transactional process, the object states in memory become stale and out of
        # sync with the db. refresh method will allow us to update to object state
        # from the latest db, ensuring it reflects the current state of the row

        return new_category

    except HTTPException:
        raise  # this data already exoist thing not necessarily an info we wanna log
    except Exception as e:
        db.rollback
        logger.error(f"Unexpected error while creating category: {e}")
        # dev.log da belirecek error i buraya yazdik
        raise HTTPException(status_code=500, detail="Internal server errorrr")


"""
@router.post("/", response_model=CategoryReturn, status_code=201): 
This is a decorator that marks the function below it (create_category) as a 
POST request handler for the specified route ("/"). It also specifies that 
the expected response model is CategoryReturn and sets the HTTP status code 
to 201 (Created) for successful requests.

def create_category(category_data: CategoryCreate, 
db: Session = Depends(get_db_session)):: This is the function definition for 
the route handler. It takes two parameters:
- category_data: This parameter is annotated with CategoryCreate, indicating
that the handler expects data in the format defined by the CategoryCreate 
model. This likely represents the data submitted by the client to create a 
new category.
- db: This parameter represents a database session. It's annotated with 
Depends(get_db_session), indicating that it's a dependency injected by 
FastAPI using the get_db_session function. This function is likely 
responsible for providing a database session to the route handler.

Inside the function:

new_category = Category(**category_data.model_dump()): This line creates a 
new instance of the Category model using the data provided in category_data. 
It likely uses the model_dump() method of the CategoryCreate model to 
extract the relevant data for creating a new category.

"""

"""
Dependency Injection:
Dependency injection is a design pattern where dependencies (such as database
connections, configuration settings, or other objects) are provided to a 
component (such as a class or function) from the outside, rather than being 
created or managed internally. In the context of FastAPI, dependency 
injection is used extensively to provide dependencies to route handler 
functions. For example, in FastAPI, you can declare dependencies using the 
Depends function, and FastAPI will automatically inject the required 
dependencies when the route handler is invoked.
"""


"""
In the context of the code you provided,
new_category = Category(**category_data.model_dump()) is creating a new
instance of the Category class using data extracted from the category_data 
object. This is possible because the ** syntax in Python is used for 
unpacking dictionaries into keyword arguments. The category_data.model_dump()
likely returns a dictionary containing data that can be used to initialize a 
Category object. By unpacking this dictionary and passing it as keyword 
arguments to the Category constructor, a new Category instance is created 
with the provided data.

Yes, you can indeed pass another class inside a class. This is often used for creating relationships between classes in object-oriented programming. In your example, the parent_id column of the Category class is a foreign key that references the id column of the same Category class. This establishes a relationship between different instances of the Category class, allowing for hierarchical structures where one category can be a parent of another.
"""


# Endpoint to delete a category
@router.delete("/{category_id}", response_model=CategoryDeleteReturn)
def delete_category(category_id: int, db: Session = Depends(get_db_session)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db.delete(category)
        db.commit()
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Endpoint to update an existing category
@router.put("/{category_id}", response_model=CategoryReturn, status_code=201)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db_session),
):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        for key, value in category_data.model_dump().items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
