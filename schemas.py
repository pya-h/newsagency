from typing import Tuple

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    item_class: str
    body: str
    view_counter: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserClassesUpdate(BaseModel):
    classes: list[str]


class UserGetItems(BaseModel):
    items: list[Item]


class User(UserBase):
    id: int
    is_active: bool
    classes: str

    class Config:
        orm_mode = True
