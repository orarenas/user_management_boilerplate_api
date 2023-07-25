from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(String(100), nullable=False)
    role_description = Column(Text, nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)
    #updated_by = Column(String(100), nullable=True)

    role_permissions = relationship("RolePermissions", back_populates="role")
    user_roles = relationship("UserRoles", back_populates="role")

class PermissionCategory(Base):
    __tablename__ = "permission_category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    permission_category = Column(String(100), nullable=False)
    permission_category_description = Column(Text, nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)
    #updated_by = Column(String(100), nullable=True)

    permission = relationship("Permission", back_populates="permission_category")

class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    permission = Column(String(100), nullable=False)
    permission_description = Column(Text, nullable=False)
    permission_category_id = Column(Integer, ForeignKey("permission_category.id"))
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)
    #updated_by = Column(String(100), nullable=True)

    permission_category = relationship("PermissionCategory", back_populates="permission")
    role_permissions = relationship("RolePermissions", back_populates="permission")

class RolePermissions(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    permission_id = Column(Integer, ForeignKey("permission.id"))
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)
    #updated_by = Column(String(100), nullable=True)

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")