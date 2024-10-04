from sqlalchemy import Boolean, DateTime, Float, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

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
    assert db_inspector.has_table("product_line")
    # this is also a way to test if migration worked correctly


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "product_line"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["price"]["type"], type(Numeric(precision=5, scale=2)))
    # bu 5 ve 2 diagramda belirtilmis, the value can store up to 5 digits in total, 2 of them as decimal points
    assert isinstance(
        columns["sku"]["type"], UUID
    )  # diger uuid buna gore daha uzun bipreicifctiondi
    assert isinstance(columns["stock_qty"]["type"], Integer)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(
        columns["order"]["type"], Integer
    )  # bunun integer oldugunu nerden anladi anlamadim
    # sagdaki additional a tiklayinca yaziyomus order between 1 and 20 diye
    assert isinstance(
        columns["weight"]["type"], Float
    )  # he said weight can be definitely his own table so float diyelim ?
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["product_id"]["type"], Integer)


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_line"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "price": False,
        "sku": False,
        "stock_qty": False,
        "is_active": False,
        "order": False,
        "weight": False,
        "created_at": False,
        "product_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


"""
- [ ] Ensure that column foreign keys correctly defined.
"""


def test_model_structure_foreign_key(db_inspector):
    table = "product_line"
    foreign_keys = db_inspector.get_foreign_keys(table)
    """
    This is what the output to get_foreign_keys look like:
[
    {
        "name": "fk_order_customer_id",
        "constrained_columns": ["customer_id"],
        "referred_table": "customers",
        "referred_columns": ["id"],
        "on_update": "CASCADE",
        "on_delete": "CASCADE",
        # Other metadata...
    },
    # Other foreign key constraints...
]
    
    """
    print(foreign_keys)
    product_foreign_key = next(
        (fk for fk in foreign_keys if set(fk["constrained_columns"]) == {"product_id"}),
        None,
    )  # this line searches the foreign key constaints associated to product_id column
    # sanirim set deme sebebi birden fazla kez product_id, product_id... return edebiliyo
    # ya da haa sey, sol taraf list karsi taraf set diye de olabilir simdi
    assert product_foreign_key is not None


# I think if we had multiple foreign keys, we would have been running this test for each of them

"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.

"""


def test_model_structure_column_constraints(db_inspector):
    table = "product_line"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "product_order_line_range" for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_line_max_value" for constraint in constraints
    )  # 999.99 dan buyuk olamamasini yazcaz aslinda 5 digit 2 decimal in dogal sonucu bi yandan


# we ll go models.py and add CheckConstraint class of sqlalchey

"""
- [ ] Verify the correctness of default values for relevant columns.
specied by DV in the database
"""


def test_model_structure_default_values(db_inspector):
    table = "product_line"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["stock_qty"]["default"] == "0"
    assert columns["is_active"]["default"] == "false"


"""
- [ ] Ensure that column lengths align with defined requirements.

"""


# bu sefer column length ile alakali bi sey yok


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.

"""


def test_model_structure_unique_constraints(db_inspector):
    table = "product_line"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_line_sku" for constraint in constraints
    )  # aslinda bu uuid type oldugu icin ayni denk gelmesi cok dusuk ihtimalmis ama yine deymis
    # uuid is sth generated automatically galiba
    assert any(
        constraint["name"]
        == "uq_product_line_order_product_id"  # order and product_id together
        for constraint in constraints
    )  # bu her bi product_id ye bagli 1 order olmasini sagliyo
    # o waman her bi product_id icin maksimum 20 tane mi product line id olcak demek bu


# models.py a gidip tek tek bunlarin hepsini build et simdi
