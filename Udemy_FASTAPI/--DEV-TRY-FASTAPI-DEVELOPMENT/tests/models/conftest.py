from fixtures import db_inspector  # noqa: F401

# so whenever we run tests in this models folder, this conftest file ensures that
# the inpector will get initiated
# (we re gonna make available the fixture in this folder)
