from typing import AnyStr, List, Dict
from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    username: AnyStr
    name: AnyStr
    email: EmailStr


class UserLogin(BaseModel):
    username: AnyStr
    password: AnyStr

