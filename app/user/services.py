from app.user import models
from app.auth.services import get_password_hash

from sqlalchemy.orm import Session

from app.user.schemas import UserCreate, UserRolesCreate, UpdateUserActiveRole

class UserManager(object):
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, id: int):
        return db.query(models.User).filter(models.User.id == id).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        new_user = models.User(**user.model_dump())

        new_user.hashed_password = get_password_hash(new_user.hashed_password)

        db.add(new_user)
        db.commit()
        return new_user
    
    @staticmethod
    def update_user_active_role(db: Session, user_id: int, user: UpdateUserActiveRole):
        stored_item_data = db.query(models.User).filter(models.User.id == user_id).first()
        update_data = user.model_dump(exclude_unset=True)
        db.query(models.User).filter(models.User.id == user_id).update(update_data, synchronize_session=False)

        db.commit()
        db.refresh(stored_item_data)
        return stored_item_data
    
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