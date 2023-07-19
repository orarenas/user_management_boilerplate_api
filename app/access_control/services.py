from app.access_control import models

from sqlalchemy.orm import Session

from app.access_control.schemas import RoleCreate, PermissionCreate, PermissionCategoryCreate, RolePermissionsCreate

class RoleManager(object):
    @staticmethod
    def get_all_roles(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Role).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_role(db: Session, role: RoleCreate):
        new_role = models.Role(**role.dict())

        db.add(new_role)
        db.commit()
        return new_role
    
class PermissionManager(object):
    @staticmethod
    def get_all_permission_categories(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.PermissionCategory).order_by(models.PermissionCategory.id.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_permission_category(db: Session, permission_category: PermissionCategoryCreate):
        new_permission_category = models.PermissionCategory(**permission_category.dict())

        db.add(new_permission_category)
        db.commit()
        return new_permission_category

    @staticmethod
    def get_all_permissions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Permission).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_permission(db: Session, permission: PermissionCreate):
        new_permission = models.Permission(**permission.dict())

        db.add(new_permission)
        db.commit()
        return new_permission
    
class RolePermissionsManager(object):
    @staticmethod
    def get_all_role_permissions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.RolePermissions).order_by(models.RolePermissions.id.asc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_role_permissions(db: Session, role_id: int):
        return db.query(models.RolePermissions).filter(models.RolePermissions.role_id == role_id).order_by(models.RolePermissions.permission_id.asc()).all()
    
    @staticmethod
    def create_role_permissions(db: Session, role_permission: RolePermissionsCreate):
        new_role_permission = models.RolePermissions(**role_permission.dict())

        db.add(new_role_permission)
        db.commit()
        return new_role_permission