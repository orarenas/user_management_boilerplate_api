from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Annotated
from pydantic import ValidationError

from jose import JWTError,jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from app.user.models import User
from app.auth.schemas import TokenData
from app.auth.config import Settings

from app.deps import get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#CRYPTOGRAPHY CONTEXT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#TOKEN SCHEME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={"me": "Read information about the current user.", "items": "Read items."})

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_authenticated(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(user: User, password: str):
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.authjwt_secret_key, algorithm=Settings.authjwt_algorithm)
    return encoded_jwt

""" def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=2)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, Settings.authjwt_refresh_secret_key, algorithm=Settings.authjwt_algorithm)
    return encoded_jwt """

async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, Settings.authjwt_secret_key, algorithms=[Settings.authjwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes,username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user_authenticated(token_data.username, db)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return token_data

async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=["me"])]):
    """ if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user") """
    return current_user

async def get_sample(current_user: Annotated[User, Security(get_current_user, scopes=["me"])]):
    """ if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user") """
    return current_user

