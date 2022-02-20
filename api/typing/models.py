from typing import AnyStr, List, SupportsInt
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    username: AnyStr
    name: AnyStr
    email: EmailStr


class UsersOut(BaseModel):
    users: List[UserOut]


class UserLogin(BaseModel):
    username: AnyStr
    password: AnyStr


class CategoryOut(BaseModel):
    id: int
    name: AnyStr
    color: AnyStr


class CategoriesOut(BaseModel):
    categories: List[CategoryOut]
