from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.access_control.schemas import RoleOnly

class UserRolesBase(BaseModel):
    default_role: bool
    date_created: datetime
    created_by: str

class UserRolesCreate(UserRolesBase):
    user_id: int
    role_id: int

class UserRoles(UserRolesBase):
    id: int
    role: RoleOnly 

    class Config:
        orm_mode = True

class UserPermissions(BaseModel):
    role: RoleOnly

    class Config:
        orm_mode = True

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
    role: RoleOnly = []

    class Config:
        orm_mode = True    

class UserAuthenticate(User):
    hashed_password: str