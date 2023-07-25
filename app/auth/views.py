import os
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.orm import Session

from app.deps import get_db

from app.auth.schemas import Token
from app.auth.services import authenticate_user, get_user_authenticated, create_access_token, get_current_active_user, get_quality_procedure

from app.user.schemas import User

from datetime import timedelta

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    logged_user = get_user_authenticated(form_data.username, db)
    user = authenticate_user(logged_user, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login details",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=60      )
    access_token = create_access_token(data={"sub":  user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"} 

@auth_router.post("/logout")
async def logout(response: Response):
    return {"access_token": response.delete_cookie("access_token"), "token_type": "bearer"} 

@auth_router.get(
    "/users/me/",
    response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@auth_router.get(
    "/sample/")
async def read_sample(current_user: Annotated[User, Depends(get_quality_procedure)]):
    return current_user
