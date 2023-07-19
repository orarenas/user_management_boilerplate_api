from typing import List
from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.access_control.schemas import Role, RoleCreate, Permission, PermissionCreate, PermissionCategory, PermissionCategoryCreate, RolePermissions, RolePermissionsCreate
from app.access_control.services import RoleManager, PermissionManager, RolePermissionsManager
from app.deps import get_db

access_control_router = APIRouter()

@access_control_router.get(
    "/roles",
    response_model=List[Role],
    status_code=status.HTTP_200_OK
)
def get_all_roles(db: Session = Depends(get_db)):
    return RoleManager.get_all_roles(db)

@access_control_router.post(
    "/roles",
    response_model=Role,
    status_code=status.HTTP_201_CREATED
)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return RoleManager.create_role(db, role)

@access_control_router.get(
    "/permission-categories",
    response_model=List[PermissionCategory],
    status_code=status.HTTP_200_OK
)
def get_all_permission_categories(db: Session = Depends(get_db)):
    return PermissionManager.get_all_permission_categories(db)

@access_control_router.post(
    "/permission-categories",
    response_model=PermissionCategory,
    status_code=status.HTTP_201_CREATED
)
def create_permission_category(permission_category: PermissionCategoryCreate, db: Session = Depends(get_db)):
    return PermissionManager.create_permission_category(db, permission_category)

@access_control_router.get(
    "/permissions",
    response_model=List[Permission],
    status_code=status.HTTP_200_OK
)
def get_all_permissions(db: Session = Depends(get_db)):
    return PermissionManager.get_all_permissions(db)

@access_control_router.post(
    "/permissions",
    response_model=Permission,
    status_code=status.HTTP_201_CREATED
)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return PermissionManager.create_permission(db, permission)

@access_control_router.get(
    "/role-permissions",
    response_model=List[RolePermissions],
    status_code=status.HTTP_200_OK
)
def get_all_role_permissions(db: Session = Depends(get_db)):
    return RolePermissionsManager.get_all_role_permissions(db)

@access_control_router.get(
    "/role-permissions/{role_id}",
    response_model=List[RolePermissions],
    status_code=status.HTTP_200_OK
)
def get_role_permissions(role_id: int, db: Session = Depends(get_db)):
    return RolePermissionsManager.get_role_permissions(db, role_id)

@access_control_router.post(
    "/role-permissions",
    response_model=RolePermissions,
    status_code=status.HTTP_201_CREATED
)
def create_role_permission(role_permission: RolePermissionsCreate, db: Session = Depends(get_db)):
    return RolePermissionsManager.create_role_permissions(db, role_permission)