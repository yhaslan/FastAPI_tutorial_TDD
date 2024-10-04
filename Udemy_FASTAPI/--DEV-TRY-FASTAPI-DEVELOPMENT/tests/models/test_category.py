"""
## Table and Column Validation

Categories table visualizes relationship between category names, their hierarchies etc
Mesela one category can be electronics, another can be TVs, there will be a hierarchy btw them
Then Sony can be a further category...
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("category")
    # this is also a way to test if migration worked correctly


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""
from sqlalchemy import Boolean, Integer, String


def test_model_structure_column_data_types(db_inspector):
    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)

    # bunu o columnlari build etmeden run edince the test fails and stops
    # ilk basta cunku sadece id column u build etmistik category table icin
    # go to models.py and actually build these columns
    # then you ll have to do a new migration to make this revisions in the table
    # adina initial diyebiliriz ve varolan migrationi silip yerine bunu run edebilirz simdilik ama live db de calisirken oyle yhapmlicaz


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_constraints(db_inspector):
    table = "category"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
        "slug": False,
        "is_active": False,
        "level": False,
        "parent_id": True,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


# The comma at the end of the assert statement allows the assertion error message to be
# provided. It separates the condition being asserted from the error message.

# again it fails when we run test bcz we havent created the right setup in the model to ensure this yet

"""
- [ ] Ensure that column foreign keys correctly defined.
"""


def test_model_structure_foreign_key(db_inspector):
    table = "category"
    foreign_keys = db_inspector.get_foreign_keys(table)
    category_foreign_key = next(
        (fk for fk in foreign_keys if set(fk["constrained_columns"]) == {"parent_id"}),
        None,
    )
    assert category_foreign_key is not None


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
- name length check and slug length check are two constraints
- we ll check for unique constraints later in the end so here we r dealing with any other constraints non unique
"""


def test_model_structure_column_constraints(db_inspector):
    table = "category"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "category_name_length_check" for constraint in constraints
    )  # here we are not testing the actual constraint yet, we r just checking if it exists
    assert any(
        constraint["name"] == "category_slug_length_check" for constraint in constraints
    )


# we ll go models.py and add CheckConstraint class of sqlalchey

"""
- [ ] Verify the correctness of default values for relevant columns.
specied by DV in the database
"""


def test_model_structure_default_values(db_inspector):
    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert (
        columns["is_active"]["default"] == "false"
    )  # burda kucuk harfle yazmamiza ragmen geciyo cok garip
    assert columns["level"]["default"] == "100"

    # when it comes to db build there are 2 approaches to set default value; see in models.py
    # this test is for server_default parameter


"""
- [ ] Ensure that column lengths align with defined requirements.
burda kastettigi karakter length :  name and slug
slug ne bilmiyorum ama when we create a name slug is created from that name dedi 
ve chunklar falan dedi... bu defining lenth olayi storage optimizationa da yariyomus
yaptigi aciklama tam tersi ama 100 karakteri doldurmasanda o storage i kullanmis oluyosun dedi ne mana
"""


def test_model_structure_column_lengths(db_inspector):
    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
    assert columns["slug"]["type"].length == 120


# bu test icin zaten modele coktan koymustuk bu ozellikleri; o yuzden migrationsiz run edebiliriz

"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
reauirement larda slug column unda goruyoruz UNQ yaziyo
depends on the purpose of use
slug ornegi olarak big-red-shoe dedi, slug isimlerin api endpoint haline getirilmesi mi demek?
neyse iste boyle api endpoint gibi kullancagimiz durumlarda unique olmasini istermisiz category search icin

 slug is the part of a URL that identifies a particular page on a website in an easy-to-read form. 
 In other words, it’s the part of the URL that explains the page’s content.
 
 salak adam simdi de diyo ki if we look at additional inforlation there is an additional unique constraint
 for name and level fields, bu blankdiyagramdaki category table in sagindaki imge'ye basinca cikiyo
 
 mantikli yani bi zahmet category name unique olsun da level niye unique ya? level hiearchy yi gostermiyo mudu
 HAAAA we dont want two cat with the same name at the same level dedi, farkli levelllarda olur mu
 
 Together they must be unique (not separetly)
 
 so 1 unique constraint is for slug and 1 unique constqint for the combo of level name
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "category"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_category_name_level" for constraint in constraints
    )
    assert any(constraint["name"] == "uq_category_slug" for constraint in constraints)


# models.py a UniqueConstraint class i da ekle importa
