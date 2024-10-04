from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints


class CategoryBase(BaseModel):  # inherit the base model
    name: Annotated[
        str, StringConstraints(min_length=1)
    ]  # bu constrainti schema levelda da check edebilme sekli
    # Annotated is used to add additional metadata, in this case constraints, to this type field
    slug: Annotated[str, StringConstraints(min_length=1)]
    is_active: Optional[bool] = False
    # default value'leri oldugu icin models.pyda; bunlari boyle optional yazabiliyoruz
    level: Optional[int] = 100
    parent_id: Optional[int] = None


# simdi OOP'nin inheritanec feature u sayesinde CategoryCreate i yaratcaz
# bu base class dan inherit edecek


class CategoryCreate(CategoryBase):
    pass


# ilerde mesela extraction icin bi class yaratinca orda id field inin da olmasini eklicez
# bu sadece insert new category oldugundan bunda direkt pass


class CategoryReturn(CategoryBase):
    id: int


class CategoryUpdate(CategoryBase):
    pass


class CategoryDeleteReturn(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=1)]
