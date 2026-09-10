
from werkzeug.security import generate_password_hash , check_password_hash
from typing import Annotated
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status , Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import  UserModel
from schemas import  UserCreateSchema,UserLoginSchema
from config import security , config

SessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@router.post(
    "",
    summary="Create User",
    status_code = status.HTTP_201_CREATED,
)
async def create(
    data: UserCreateSchema,
    session: SessionDep
):
    new_user = UserModel(
        username = data.username,
        password_hash = generate_password_hash(data.password),
        email = data.email,
        created_at = date.today(),
    )
    session.add(new_user)
    await session.commit()

    return {
        "success": True,
        "message": "User creation successful",
    }

@router.post(
    "/login",
    summary = "Authorization User"
)
async def Authorization_user(
    data: UserLoginSchema,
    session: SessionDep,
    response : Response
):
    user_db = select(UserModel).where(UserModel.username == data.username)
    result = await session.execute(user_db)
    user = result.scalar_one_or_none()
    if user is None :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password or login",
        )

    password_check = check_password_hash(user.password_hash, data.password)
    if password_check == False:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password or login",
        )
    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME,token)
    return {
        "access_token" : token,
        "success": True,
        "message": "Authorization successful",
    }
