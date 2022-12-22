from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    is_superuser: bool = False


class UserCreate(UserBase):
    email: EmailStr

class UserUpdate(UserBase):
    pass

class UserInDbBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class User(UserInDbBase):
    pass

