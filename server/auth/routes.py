from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import read_config
from ..database import get_session
from .crud import create_new_user, get_user_by_id
from .dependencies import get_current_user
from .schemas import AuthToken, User, UserCreate
from .utils import authenticate_user, create_access_token, get_password_hash

router = APIRouter(prefix="/auth")


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user.hashed_password = get_password_hash(user.hashed_password)
    user = await create_new_user(session, user)
    return user


@router.get("/users/", response_model=User, dependencies=[Depends(get_current_user)])
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(session, user_id)
    return user


@router.post("/login/", response_model=AuthToken)
async def login_for_access_token(
    session: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=read_config("access_token_expire_minutes"))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
