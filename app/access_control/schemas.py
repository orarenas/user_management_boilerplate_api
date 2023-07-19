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
        from_attributes = True

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
        from_attributes = True

class PermissionDescription(BaseModel):
    permission: str
    permission_description: str

    class Config:
        from_attributes = True

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
        from_attributes = True

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
        from_attributes = True