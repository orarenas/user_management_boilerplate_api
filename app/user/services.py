from app.user import models
from app.auth.services import get_password_hash

from sqlalchemy.orm import Session

from app.user.schemas import UserCreate, UserRolesCreate

class UserManager(object):
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        new_user = models.User(**user.model_dump())

        new_user.hashed_password = get_password_hash(new_user.hashed_password)

        db.add(new_user)
        db.commit()
        return new_user
    
class UserRolesManager(object):
    @staticmethod
    def get_all_users_roles(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.UserRoles).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user_role(db: Session, user_role: UserRolesCreate):
        new_user_role = models.UserRoles(**user_role.model_dump())

        db.add(new_user_role)
        db.commit()
        return new_user_role