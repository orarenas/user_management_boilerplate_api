from datetime import datetime
from pydantic import BaseModel
from typing import List

class PermissionCategoryBase(BaseModel):
    permission_category: str
    permission_category_description: str
    date_created: datetime
    created_by: str

class PermissionCategoryCreate(PermissionCategoryBase):
    pass

class PermissionCategory(PermissionCategoryBase):
    id: int

    class Config:
        orm_mode = True

class PermissionBase(BaseModel):
    permission: str
    permission_description: str
    date_created: datetime
    created_by: str

class PermissionCreate(PermissionBase):
    permission_category_id: int

class Permission(PermissionBase):
    id: int
    permission_category: PermissionCategory = []

    class Config:
        orm_mode = True

class PermissionOnly(BaseModel):
    permission: str
    
    class Config:
        orm_mode = True

class PermissionDescription(BaseModel):
    permission: str
    permission_description: str

    class Config:
        orm_mode = True

class RolePermissionsBase(BaseModel):
    date_created: datetime
    created_by: str

class RolePermissionsCreate(RolePermissionsBase):
    role_id: int
    permission_id: int

class RolePermissions(RolePermissionsBase):
    id: int
    permission: PermissionDescription = []

    class Config:
        orm_mode = True

class RolePermissionsOnly(BaseModel):
    permission: PermissionOnly = []

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    role: str
    role_description: str
    date_created: datetime
    created_by: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    role_permissions: List[RolePermissions] = []

    class Config:
        orm_mode = True

class RoleOnly(BaseModel):
    role: str
    role_permissions: List[RolePermissionsOnly] = []

    class Config:
        orm_mode = True

# TEMPORARY CLASS NAME
class RoleName(BaseModel):
    id: int
    role: str

    class Config:
        orm_mode = True
