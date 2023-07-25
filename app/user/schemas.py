from typing import List
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    date_created: datetime
    created_by: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True    

class UserAuthenticate(User):
    hashed_password: str

class UserRolesBase(BaseModel):
    role_id: int
    date_created: datetime
    created_by: str

class UserRolesCreate(UserRolesBase):
    user_id: int