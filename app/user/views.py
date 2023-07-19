from typing import List
from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.user.schemas import User, UserCreate
from app.user.services import UserManager
from app.deps import get_db

user_router = APIRouter()

@user_router.get(
    "",
    response_model=List[User],
    status_code=status.HTTP_200_OK
)
def get_all_users(db: Session = Depends(get_db)):
    return UserManager.get_all_users(db)

@user_router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserManager.create_user(db, user)