import pytest
from sqlalchemy import inspect

# we re gonna create a code for connecting the db and passing over the inspect tool
# multiple tests gonna need this setup
# so instead of duplicating all the time, we re gonna instead extract any duplicated code into fixture
# so we can then share it with any test that needs it (the inspect tool setup)


# previously we used session for scope, now it is function
# this means this is only gonna be run when we call this fixture
@pytest.fixture(scope="function")
def db_inspector(db_session):
    return inspect(db_session().bind)


# notice we dont need to import db_session because it is set to autouse in the original fixtures.py
# so it is automatically created whenerver we create a new session so its always available for all fixtures
#### hmmmm
# so that is already a onnection  to db which can then be used by the inspect tool

# ama simdi de dedi ki we re gonna need to return a session so that inspector can actually run ve simdi
# diger fixture de degisiklik yapmaya gidiyoruz Session Local diye bi sey yaratcaz :D
