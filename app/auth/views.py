import os
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.orm import Session

from app.deps import get_db

from app.auth.schemas import Token, RefreshToken
from app.auth.services import authenticate_user, get_user_authenticated, create_access_token, create_refresh_token, get_current_active_user, get_quality_procedure

from app.user.schemas import User

from datetime import timedelta

#sample
from jose import jwt, JWTError
from app.auth.config import Settings

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
    
    access_token_expires = timedelta(minutes=0.5)
    refresh_token_expires = timedelta(minutes=2)
    access_token = create_access_token(data={"sub":  user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub":  user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"} 

@auth_router.post("/refresh")
async def refresh_token(refresh_token: RefreshToken):
    #need to find decorator
    try:
        payload = jwt.decode(refresh_token.refresh_token, Settings.authjwt_refresh_secret_key, algorithms=[Settings.authjwt_algorithm])
        access_token = create_access_token(data={"sub":  payload.get("sub")}, expires_delta=timedelta(minutes=0.5))
        refresh_access_token = create_refresh_token(data={"sub": payload.get("sub")}, expires_delta=timedelta(minutes=1))

        return {"access_token": access_token, "refresh_token": refresh_access_token, "token_type": "bearer"}
    except JWTError:
        return {"error": "Invalid refresh token"}

@auth_router.post("/logout")
async def logout(response: Response):
    return {"access_token": response.delete_cookie("access_token"), "refresh_token": response.delete_cookie("access_token"), "token_type": "bearer"} 

@auth_router.get(
    "/users/me/",
    response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@auth_router.get(
    "/sample/")
async def read_sample(current_user: Annotated[User, Depends(get_quality_procedure)]):
    return current_user
