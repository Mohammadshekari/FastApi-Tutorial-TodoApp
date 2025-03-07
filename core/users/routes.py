from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token
from core.database import get_db
from users.schemas import *
from users.models import UserModel

router = APIRouter(tags=["users"])


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj: UserModel | None = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user doesn't exists!")
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid password")

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(content={
        "detail": "logged in successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
    })


@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='username already exists!')
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail": "users registered successfully"})


@router.post("/refresh")
async def user_refresh_token(request: UserRefreshTokenSchema, db: Session = Depends(get_db)):
    user_id = decode_refresh_token(request.refresh_token)
    access_token = generate_access_token(user_id=user_id)
    return JSONResponse(content={"access_token": access_token})
