from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from cruds import auth as auth_cruds
from routers.item import DbDependency
from schemas import UserCreate, UserResponse, Token
from database import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


DbDependency = Annotated[Session, Depends(get_db)]
FormDependency = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),  # 本当は Depends(OAuth2PasswordRequestForm)] だが、第一引数と同じなので Depends() の引数は省略可能
]


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(db: DbDependency, user_create: UserCreate):
    return auth_cruds.create_user(db, user_create)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def loign(db: DbDependency, form_data: FormDependency):
    user = auth_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = auth_cruds.create_access_token(
        user.username, user.id, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
