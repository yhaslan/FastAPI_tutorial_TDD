from sqlalchemy import (
    DECIMAL,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,  # this one is object type
    UniqueConstraint,
    func,
    text,  # this one is a function to detect SQL expressions within our python code and execute as such
)
from sqlalchemy.dialects.postgresql import UUID

from .db_connetion import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default="100", server_default="100")
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    # to set the default value there are two approaches: default parameter and server default parameter
    # server default value specifies the default value applied at the database level
    # so database will utilize this and checks the default value fo that field
    # whereas default option specifies the default value that is applied at the python object level
    # in other words, application level
    # we can assign both at the same time up to you (peki ikisi hep ayni mi anlamadim)
    # but for now we re onlhy building a test to test server default

    # level field specifies the hierarchies (henuz tam anlamadim but integer)
    # 100 is used to tell we have not yet assigned any number to that

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0", name="category_name_length_check"
        ),  # name when inserted isnt blank
        # anlamadim " " yapsa length 1 cikmicak mi, e zaten "" yapmasi da nullable false ile engellenmedi mi
        CheckConstraint("LENGTH(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint(
            "name", "level", name="uq_category_name_level"
        ),  # check together
        UniqueConstraint("slug", name="uq_category_slug"),
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    pid = Column(
        UUID(as_uuid=True),  # burayi tam anlamiyorum ztn uuid ne demek ki abi
        # basta buraya unique=true da yazmis ama hata verdi cunku unique testi iki kere yapmis gibi oluyo
        # sonra aynisini productline da da yapmis onu da duzeltti
        nullable=False,
        server_default=text("uuid_generate_v4()"),  # bu gene bi sql function
    )
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="False")
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )  # as default value we re asking the sqlalchemy to generate it for us
    # this CURRENT_TIMESTAMP refers to a built-in function inside PostgreSQL db that returns current date and time
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),  # bcz unlike created_at we want this to run everytime
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    stock_status = Column(
        Enum("oos", "is", "obo", name="status_enum"),  # obo means on back order
        nullable=False,
        server_default="oos",
    )

    ### foreign key leri tanimliycaz bu step yeni
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    seasonal_event = Column(Integer, ForeignKey("seasonal_events.id"), nullable=True)
    # seasonal_event table'i build etmeden migration yapinca bu kisimdan dolayi referenced tavle error vercek

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("name", name="uq_product_name"),
        UniqueConstraint("slug", name="uq_product_slug"),
        UniqueConstraint("pid", name="uq_product_pid"),
    )


class ProductLine(Base):
    __tablename__ = "product_line"

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)  # decimal type boyle buyuk harfleymis
    sku = Column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )  # we kept the same setup for this uuid as above
    stock_qty = Column(Integer, nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    order = Column(Integer, nullable=False)
    weight = Column(
        Float,
        nullable=False,
    )
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    ## simdi constraint ve unique cpnstraintleri yazcaz kolumnlar icin

    __table_args__ = (
        CheckConstraint(
            "price >= 0 AND price <= 999.99", name="product_line_max_value"
        ),  # anlamadim bunda price ayrica bi tirnaga alinmamis ama asagida order alinmis niye
        CheckConstraint(
            '"order" >= 1 AND "order" <= 20', name="product_order_line_range"
        ),
        # ogrendim cunku order is a reserved keyword in sql therefore we need to wrap it
        # in double quote to use it as a column name.
        # diger turlu denedigimizde all 21 tests fail
        # why all? because in order for any test to run we first need that all tables created properly
        ##### Ayrica "''" sirasiyla double yapinca da hata veriyo, '""' olunca calisiyo
        UniqueConstraint(
            "order", "product_id", name="uq_product_line_order_product_id"
        ),
        UniqueConstraint("sku", name="uq_product_line_sku"),
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, nullable=False)
    alternative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            '"order" >= 1 AND "order" <= 20', name="product_image_order_range"
        ),
        CheckConstraint(
            "LENGTH(alternative_text) > 0",
            name="product_image_alternative_length_check",
        ),
        CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        UniqueConstraint(
            "order", "product_line_id", name="uq_product_image_order_product_line_id"
        ),
    )


class SeasonalEvents(Base):
    __tablename__ = "seasonal_events"

    id = Column(Integer, primary_key=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="seasonal_event_name_length_check",
        ),
        UniqueConstraint("name", name="uq_seasonal_event_name"),
    )


class Attributes(Base):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="attribute_name_length_check",
        ),
        UniqueConstraint("name", name="uq_attribute_name"),
    )


class ProductType(Base):
    __tablename__ = "product_type"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    parent = Column(Integer, ForeignKey("product_type.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_type_name_length_check"),
        UniqueConstraint("name", "level", name="uq_product_type_name_level"),
    )


class AttributeValue(Base):
    __tablename__ = "attribute_value"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value = Column(String(100), nullable=False)
    attribute_id = Column(Integer, ForeignKey("attributes.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(attribute_value) > 0", name="attribute_value_length_check"
        ),  # basta parantezin icini name unutmusum diye hata verdi cozduk
        UniqueConstraint(
            "attribute_value", "attribute_id", name="uq_attribute_value_value_id"
        ),
    )


class ProductLineAttributeValue(Base):
    __tablename__ = "product_line_attribute_value"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value_id = Column(
        Integer, ForeignKey("attribute_value.id"), nullable=False
    )
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "attribute_value_id",
            "product_line_id",
            name="uq_attribute_value_product_line_id",
        ),
    )


class ProductProductType(Base):
    __tablename__ = "product_product_type"

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_type.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "product_type_id",
            name="uq_product_product_type_id",
        ),
    )
