from typing import List
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr


class UsersOut(BaseModel):
    users: List[UserOut]


class UserLogin(BaseModel):
    username: str
    password: str


class CategoryIn(BaseModel):
    name: str
    color: str


class CategoryOut(BaseModel):
    id: int
    name: str
    color: str


class CategoriesOut(BaseModel):
    categories: List[CategoryOut]


class StoreOut(BaseModel):
    id: int
    name: str


class StoresOut(BaseModel):
    stores: List[StoreOut]


class StoreIn(BaseModel):
    name: str


class StoresIn(BaseModel):
    stores: List[StoreIn]
