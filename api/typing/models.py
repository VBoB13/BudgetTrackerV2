from typing import Dict, List
from pydantic import BaseModel, EmailStr

from api.objects import subscriptions


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


class TransactionOut(BaseModel):
    id: int
    date: str
    amount: float
    currency: str
    user: str
    store: str
    comment: str


class TransactionsOut(BaseModel):
    transactions: List[TransactionOut]


class TransactionIn(BaseModel):
    date: str
    amount: float
    currency: str
    category: str
    user_id: int
    store: str
    comment: str


class SubscriptionIn(BaseModel):
    name: str
    start_date: str
    end_date: str
    cost: float
    currency: str
    auto_resub: bool
    period: str


class SubscriptionOut(SubscriptionIn):
    id: int


class SubscriptionsOut(BaseModel):
    subscriptions: List[SubscriptionOut]
