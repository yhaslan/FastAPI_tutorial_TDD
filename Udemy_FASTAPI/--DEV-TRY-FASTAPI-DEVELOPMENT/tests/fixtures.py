import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_database_container

# fixture is like a function that provides a fixed baseline for your test in pytest
# it performs a set of tasks need in your test in general such as initializing the db, maybe creating directories..
# in ptyest scope defines the lifetime and scope of that fixture
# so in this example this fixture is gonna be used once for the entire duration of this test session
# n gonna be destroyed when test session completes


@pytest.fixture(scope="session")
def db_session():
    container = start_database_container()  # this one is a create db fixture
    # autouse parameter ensures this fixture is invoked for every test function within its scope
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@127.0.0.1:5434/inventory"
    )  ############!!!!! it did not work without passing the environment variable manually
    # bunun original kodunda env filedan cekiyodu galiba yukardakini

    with engine.begin() as connection:
        # engine.begin starts a new db transaction, which is assigned to var named connection
        migrate_to_db("migrations", "alembic.ini", connection)

    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # bunu diger fixtures.py i yazarken olusturmamiz gerekti
    yield SessionLocal

    # yield function turns the fixtures function into a generator
    #### hiiic anlamadim ne diyo
    # sanirim once we finish with the session the code coming after will be run (thanks to yield)
    # so we can then perform some additional operations

    ##### HAAAA burda return desek mesela fonksiyon burda biter, oysa yield buraya kadar execute ettikten sonra
    # additional operation da yapabilmemizi sagliyo gibi bi sey glb like stop and remove the container
    # after all tests are finished !!

    # iyi ama all test finish kismindan once remove edilmesini ne engellicek ?

    # container.stop()
    # container.remove()
    engine.dispose()  # will dispose the connection pool we used for engine, to clean up everythin


@pytest.fixture(scope="function")  # fixture will be invoked once per test function
def client():
    with TestClient(app) as _client:
        yield _client

        # this is the fixture for our client which we will pass into each test
        # that requires access to http endpoint
        # anytime we make http request we r gonna need a test client
