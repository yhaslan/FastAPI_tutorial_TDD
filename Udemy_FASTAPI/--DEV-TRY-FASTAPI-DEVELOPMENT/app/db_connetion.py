import os

from sqlalchemy import create_engine  # utilized to create a db engine
from sqlalchemy.orm import declarative_base, sessionmaker

DEV_DATABASE_URL = os.getenv("DEV_DATABASE_URL")
# DEV_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/inventory"

engine = create_engine(DEV_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
# autocommit True olunca everytime we have db operatons like create insert delete
# it is automatically committed to db; we set that to False
# so we would need to manually commit ultimately
# setting to false will provid us more transaction control dedi

# flush i da anlatti ama cok onemli degil dedi su an icin, ilerde onemliymis
# kafa karistirici geldi bana

# bind True, bind parameter is used to associated the session with a spcific db engine
# if true, it will be associated to default db engine we specified in create_engine

# so it specifies that this session gonna be utilized for this engine
# you dont necessairly bin to a single db

Base = declarative_base()
# a common method to create a base class for model definitions
# it will allow us to define a db model with python classes
# each class will typically inherit from a common base class


def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
