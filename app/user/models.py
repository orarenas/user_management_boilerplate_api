from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(75), nullable=False)
    last_name = Column(String(75), nullable=False)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)

    user_roles = relationship("UserRoles", back_populates="user")

class UserRoles(Base):
    __tablename__ ="user_roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    active_role = Column(Boolean, nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_updated = Column(TIMESTAMP, nullable=True)
    created_by = Column(String(100), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")