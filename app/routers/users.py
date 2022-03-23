from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils.users import create_user, get_user_by_email, validate_password, create_user_token
from app.schemas.user import Token, UserInDB, UserRegistationRequest

router = APIRouter()

@router.post("/sign-up")
async def register_user(user_reg: UserRegistationRequest):
    result = await create_user(user_reg)

    return result

@router.post("/auth", response_model = Token)
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(email = form_data.username)
    if not user:
        raise HTTPException(status_code = 400, detail="Incorrect email or password")

    if not validate_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code = 400, detail="Incorrect email or password")

    return await create_user_token(user)