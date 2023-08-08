from typing import List
from fastapi import APIRouter, Depends, status
from typing import Annotated

from sqlalchemy.orm import Session

from app.user.schemas import User, UserCreate, UserRoles, UserRolesCreate,  UserListedRoles, UpdateUserActiveRole
from app.user.services import UserManager, UserRolesManager
from app.deps import get_db

from app.auth.services import get_current_active_user

user_router = APIRouter()

@user_router.get(
    "",
    response_model=List[User],
    status_code=status.HTTP_200_OK
)
def get_all_users(db: Session = Depends(get_db)):
    return UserManager.get_all_users(db)

# TEMPORARY ROUTE
@user_router.get(
    "/listed-roles",
    response_model=List[UserListedRoles],
    status_code=status.HTTP_200_OK
)
def get_all_users_with_roles(db: Session = Depends(get_db)):
    return UserManager.get_all_users(db)

# TEMPORARY ROUTE
@user_router.get(
    "/{user_id}/listed-roles",
    response_model=UserListedRoles,
    status_code=status.HTTP_200_OK
)
def get_user_and_roles(user_id: int, db: Session = Depends(get_db)):
    return UserManager.get_user_by_id(db, user_id)

#TEMPORARY ROUTE
@user_router.get(
    "/me",
    response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@user_router.get(
    "/{id}",
    response_model=User,
    status_code=status.HTTP_200_OK
)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return UserManager.get_user_by_id(db, id)

@user_router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserManager.create_user(db, user)

@user_router.patch(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK
)
def update_user_active_role(user_id: int, user: UpdateUserActiveRole, db: Session = Depends(get_db)):
    return UserManager.update_user_active_role(db, user_id, user)

@user_router.get(
    "/user-roles",
    response_model=List[UserRoles],
    status_code=status.HTTP_200_OK
)
def get_all_users_roles(db: Session = Depends(get_db)):
    return UserRolesManager.get_all_users_roles(db)

@user_router.post(
    "/user-roles",
    response_model=UserRoles,
    status_code=status.HTTP_201_CREATED
)
def create_user_role(user_role: UserRolesCreate, db: Session = Depends(get_db)):
    return UserRolesManager.create_user_role(db, user_role)