import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models import Category
from app.schemas.category_schema import CategoryCreate
from tests.factories.models_factory import get_random_category_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


"""
The function mock_output is a higher-order function that returns a function.
This returned function, when called, will always return the return_value provided to 
mock_output. This pattern is often used in testing scenarios, particularly when you want
to mock the behavior of a function or method.

return lambda *args, **kwargs: return_value: This part defines an anonymous lambda function that takes any number of positional and keyword arguments (*args and **kwargs). When this lambda function is called, it will simply return the return_value provided to mock_output.
Here's an example of how you might use mock_output:

# Define a mock function that always returns 42
mock_function = mock_output(return_value=42)

# Call the mock function
result = mock_function(1, 2, 3, keyword_arg='value')

# Print the result (which will always be 42)
print(result)  # Output: 42
"""


def test_unit_schema_category_validation():
    valid_data = {"name": "test category", "slug": "test-slug"}
    category = CategoryCreate(**valid_data)
    #  ** in Python is the "unpacking" operator when used in a function call.
    # It is used to unpack a dictionary or keyword arguments into individual elements
    # category = CategoryCreate(name="test category", slug="test-slug")

    # if this is succesful, if data is valid data, that is if it is validated against
    # our schema, then it means that data have been serialized
    assert category.name == "test category"
    assert category.is_active is False
    # normalde bu ikisi test etmeye yetiyo cunku digerlerine default valueler tanimlanmis
    # simdi let's go and build the schema inside the app
    assert category.level == 100
    assert category.parent_id is None
    # ama defaultlari olmasi gezrektigi gibi mi atiyo ona da bakti herhalde

    invalid_data = {
        "name": "test category",
    }
    with pytest.raises(ValidationError):
        CategoryCreate(
            **invalid_data
        )  # peki bunun slug in tanimlanmamasiyla alakasi ne ya


# this pqrt invqlidqtes data if the incorrect data is inserted diyo da
# neden name i tuttuk slug i attik? bi de bu test napiyo yani

"""
Chatgpt ile konustum, diyo ki bu fonksion aslinda bi tane valid data test;
bi tane de invalid data test ten olusuyo. valid_data dictionary yi kullanarak
bi class instance yapiyo ilkinde; gordugun gibi sadece zorunlu fieldlara value
atiyo; default bi value su olanlari ellemiyo. Elleyebilirdi de np.
Aslinda assert testte slug i unutmasi biraz salakca olmus, bi yandan evet
zaten assign eden biziz bi daha assertiona gerek yok demis olabilir ama
aynisi o zaman category icin de gecerli

invalid data ya gelince bu bi schema testi oldugundan data type uyumlu mu falan
gibi seylere henuz bakmiyoruz galiba, onun yerine zorunlu bi field missingse
invalid olmasindan bahsediyoruz. sanirim slug'in missing olmasini ornek olarak
secmis, category de missing olabilirdi galiba
category_schema ya bakarsak class soyle tanimlanmis:

class CategoryBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    slug: Annotated[str, StringConstraints(min_length=1)]
    is_active: Optional[bool] = False
    level: Optional[int] = 100
    parent_id: Optional[int] = None
    
(cateogry create direkt bundan inherit ztn)

yani zaten bu invalid_data dict i biz bu class'tan gecirince otomatik olarak
bi hata verilcek biz onu biliyoruz
gercekte slug disindaki field lara da tek tek bakmak gerekebilir gibi anladim
chatin dediginden duruma gore

This code uses a with statement along with pytest.raises to assert that 
an instance of ValidationError is raised when attempting to create a 
CategoryCreate instance with the incomplete data specified in invalid_data. 
If the expected exception (ValidationError) is not raised during the 
execution of the code inside the with block, the test will fail.


adam kendi de we could delve deeper and imagine possible edge cases that
need to test n validate dedi
"""


"""
- [ ] Test POST new category successfully
"""


def test_unit_create_new_category_successfully(client, monkeypatch):
    # burdaki client argument fixtures de tanimladigimiz client functionmis
    # biz conftest icinde sadece db_session fixture unu import etmedik mi nasil olcak

    # monkeypatch allow modify at the runtime of testing
    category = get_random_category_dict()  # ge,erate one random category

    ########## BU asagidaki iki satiri ben ekledim, sadece id'yi category dictten alip
    # diger fieldlari random generate ettim, boylece sonda response.json() == category
    # cikinca testi manual insertiondan degil post request basarili diye gectigimize eminiz
    fake_cat = get_random_category_dict()
    fake_cat["id"] = category["id"]

    for key, value in fake_cat.items():  # adam burayi koymamisti hata verdi
        monkeypatch.setattr(Category, key, value)
        # neymis bu bi id yaratiyomus guya falan filan"""

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    # this code ensures that if "sqlalchemy.orm.Query.first" operation appears in our
    # function, it is not gonna be run bcz we r overriding it
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    """
    These lines use monkeypatch.setattr() to patch specific attributes or methods. 
    In this case, they're patching SQLAlchemy's Query.first, Session.commit, and 
    Session.refresh methods with mock functions created by mock_output(). This allows you
    to control the behavior of these methods during testing by replacing them with mock
    functions that always return a predetermined value
    """

    body = category.copy()
    body.pop("id")
    """
    This creates a copy of the category dictionary and removes the "id" key 
    from it. The modified dictionary is then assigned to the body variable. 
    This likely prepares the request body to be sent in a POST request, 
    ensuring that it does not contain an id field.
    """
    response = client.post("api/category/", json=body)
    # This line makes a POST request to the "api/category/" endpoint with the
    # JSON data in the body variable. It's assumed that client is an HTTP
    # client object provided by the testing framework.

    assert response.status_code == 201
    assert response.json() == category


"""
"Patching attributes" refers to dynamically modifying attributes of an object
during runtime, typically for the purpose of testing.
In Python, you can achieve this using various techniques, such as directly 
assigning new values to attributes or using tools like unittest.mock or 
pytest's monkeypatch fixture.
For example, let's say you have a class Foo with an attribute bar:

class Foo:
    def __init__(self):
        self.bar = 42
        
obj = Foo()
print(obj.bar)  # Output: 42

obj.bar = 99  # Patching the attribute
print(obj.bar)  # Output: 99

for key, value in category.items():
    monkeypatch.setattr(Category, key, value)
This loop iterates over each key-value pair in the category dictionary. 
For each pair, it uses the monkeypatch fixture (provided by the pytest 
testing framework) to dynamically set an attribute of the Category class to 
the corresponding value.

By corresponding value, it means the Category class needs to have an attribute
already with the same name as the key of the key-value pair in category dict

BU arada BU SALAKLAR CATEGORY CLASS I APP.MODELS DEN CAGIRDI
AMA ASIL OVERWRITE EDECEGI CATEGORY CLASS SANKI FACTORYDEKIYDI
"""


"""
monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output()):
This line is patching the first method of the Query class in SQLAlchemy. 
The first method is typically used to retrieve the first result of a query. 
By using mock_output(), it's replacing the original method with a mock
function that always returns the value provided
(or None if no value is provided).

monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output()): 
Similarly, this line is patching the commit method of the Session class in 
SQLAlchemy. The commit method is used to commit the current transaction. 
Again, it's replacing the original method with a mock function that always 
returns the value provided (or None if no value is provided).

monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output()): 
This line is patching the refresh method of the Session class in SQLAlchemy. 
The refresh method is typically used to refresh the state of an object from 
the database. As before, it's replacing the original method with a mock 
function that always returns the value provided (or None if no value is 
provided).

patching the respective methods (first, commit, and refresh) with mock 
functions that always return None when invoked. This effectively simulates 
the behavior of these methods without executing their actual logic, which 
can be useful for testing purposes.

The mock_output function provided:
def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value
is indeed a custom mock function. However, it's a very simple one.

Let's break down how it works:

It takes an optional return_value argument, which defaults to None.
It returns a lambda function.
The lambda function accepts any number of positional and keyword 
arguments (*args and **kwargs), but it simply returns the return_value.
So effectively, when you call mock_output() without any arguments, 
it returns a lambda function that, when invoked, always returns None.

This is indeed a custom mock function, but it's a basic one that always 
returns the same value (None). In more complex scenarios, you might define 
mock functions that perform additional logic, such as returning different 
values based on the arguments passed to them, raising exceptions, or 
recording calls for later inspection.

"""


@pytest.mark.parametrize(
    "existing_category, category_data, expected_detail",
    [
        (True, get_random_category_dict(), "Category name and level already exists"),
        (True, get_random_category_dict(), "Category slug already exists"),
    ],
)  # bunlar galiba parameters for existing category, category_data and expected_detail
def test_unit_create_new_category_existing(
    client, monkeypatch, existing_category, category_data, expected_detail
):
    def mock_check_existing_category(
        db, category_data
    ):  # check_existing categorynin mock hali
        if existing_category:  # yukarda parameterize yaparak mi sagladik
            raise HTTPException(status_code=400, detail=expected_detail)

    monkeypatch.setattr(
        "app.routers.category_routes.check_existing_category",
        mock_check_existing_category,
    )

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    # bunda niye commit ve refresh yok,
    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)

    assert response.status_code == 400

    if expected_detail:
        assert response.json() == {"detail": expected_detail}


"""
- [ ] Test POST category db server issue
"""


def test_unit_create_new_category_with_internal_server_error(client, monkeypatch):
    category = get_random_category_dict()

    # Mock an exception to simulate an internal server error
    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    for key, value in category.items():
        monkeypatch.setattr(
            Category, key, value
        )  # gene bi attribute yoluyla manual populate hali
    # deminkinde niye bunu yapmadiysak hic
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_create_category_exception)

    body = category.copy()
    body.pop("id")
    response = client.post("/api/category/", json=body)
    assert response.status_code == 500


"""
- [ ] Test GET all categories successfully
"""


def test_unit_get_all_categories_successfully(client, monkeypatch):
    category = [get_random_category_dict(i) for i in range(5)]  # 5 oylesine sanrim
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(category))
    response = client.get("api/category/")
    assert response.status_code == 200
    assert response.json() == category


"""
- [ ] Test GET all categories with empty result
"""


def test_unit_get_all_categories_returns_empty(client, monkeypatch):
    category = []
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(category))
    response = client.get("api/category/")
    assert response.status_code == 200
    assert response.json() == category


"""
- [ ] Test GET all categories with database server error
"""


def test_unit_get_category_all_with_internal_server_error(client, monkeypatch):
    # Mock an exception to simulate an internal server error
    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_create_category_exception)
    response = client.get("api/category/")
    assert response.status_code == 500


"""
- [ ] Test GET single category by slug successfully
"""


@pytest.mark.parametrize(
    "category", [get_random_category_dict() for _ in range(3)]
)  # same test will be run 3 times with different random categories
def test_unit_get_single_category_successfully(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category))
    # what is the difference between first and all?

    response = client.get(f"api/category/slug/{category['slug']}")
    assert response.status_code == 200
    assert response.json() == category


"""
- [ ] Test GET single category slug not found
"""


@pytest.mark.parametrize("category", [get_random_category_dict() for _ in range(3)])
def test_unit_get_single_category_not_found(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    response = client.get(f"api/category/slug/{category['slug']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category does not exist"}


"""
- [ ] Test GET single category by slug internal server error
"""


@pytest.mark.parametrize("category", [get_random_category_dict() for _ in range(3)])
def test_unit_get_single_category_with_internal_server_error(
    client, monkeypatch, category
):
    # Mock an exception to simulate an internal server error
    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_create_category_exception)
    response = client.get(f"api/category/slug/{category['slug']}")
    assert response.status_code == 500


"""
- [ ] Test UPDATE category successfully
"""


def test_unit_update_category_successfully(client, monkeypatch):
    category_dict = get_random_category_dict()
    category_instance = Category(**category_dict)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category_instance))
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = category_dict.copy()
    body.pop("id")
    response = client.put(
        "api/category/1", json=body
    )  # bu da daha onceki mantikla hicbir sey test etmiyo
    assert response.status_code == 201
    assert response.json() == category_dict


"""
- [ ] Test UPDATE category not found
"""


def test_unit_update_category_not_found(client, monkeypatch):
    category_dict = get_random_category_dict()

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = category_dict.copy()
    body.pop("id")
    response = client.put("api/category/1", json=body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


"""
- [ ] Test UPDATE category internal server error
"""


def test_unit_update_category_internal_error(client, monkeypatch):
    category_dict = get_random_category_dict()

    # Mock an exception to simulate an internal server error
    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_create_category_exception)

    body = category_dict.copy()
    body.pop("id")
    response = client.put("api/category/1", json=body)
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


"""
- [ ] Test DELETE category successfully
"""


def test_unit_delete_category_successfully(client, monkeypatch):
    category_dict = get_random_category_dict()
    category_instance = Category(**category_dict)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category_instance))
    monkeypatch.setattr("sqlalchemy.orm.Session.delete", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    response = client.delete("api/category/1")
    expected_json = {"id": category_dict["id"], "name": category_dict["name"]}
    assert response.status_code == 200
    assert response.json() == expected_json


"""
- [ ] Test DELETE category not found
"""


def test_unit_delete_category_not_found(client, monkeypatch):
    category = []
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category))
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    response = client.delete("api/category/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


"""
- [ ] Test DELETE category internal server error
"""


def test_unit_delete_category_internal_error(client, monkeypatch):
    # Mock an exception to simulate an internal server error
    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_create_category_exception)

    response = client.delete("api/category/1")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
