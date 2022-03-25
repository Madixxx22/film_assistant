from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token

from app.utils.users import create_user, get_user_by_email, is_active, validate_password, create_user_token
from app.schemas.user import Token, UserRegistationRequest

router = APIRouter()

@router.post("/sign-up")
async def register_user(user_reg: UserRegistationRequest):
    try:
        result = await create_user(user_reg)
        result_auth = await create_user_token(user_reg)
    except:
        raise HTTPException(status_code = 400, detail="Such a user already exists")
    return result

@router.post("/log-in", response_model = Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(email = form_data.username)
    if not user:
        raise HTTPException(status_code = 400, detail="Incorrect email or password")

    if not validate_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code = 400, detail="Incorrect email or password")
    elif not is_active(user):
        raise HTTPException(status_code = 400, detail="Inactive user")

    return Token(access_token = await create_access_token(user))
