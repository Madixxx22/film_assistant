from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.crud_user import user_crud
from app.utils.users import get_current_active_user, validate_password
from app.schemas.user import Token, UserProfileUpdate, UserProfileResponce, UserRegistationRequest, UsersAuth

router = APIRouter()

@router.post("/sign-up")
async def register_user(user_reg: UserRegistationRequest):
    try:
        result = await user_crud.create_user(user_reg)
        result_auth = await user_crud.create_user_token(user_reg)
        result_info = await user_crud.create_user_profile(user_reg)
    except:
        raise HTTPException(status_code = 400, detail="Such a user already exists")
    return result

@router.post("/log-in", response_model = Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_crud.get_user_by_email(email = form_data.username)
    if not user:
        user = await user_crud.get_user_by_login(login = form_data.username)
        if not user:
            raise HTTPException(status_code = 400, detail="Incorrect email or password")
    if not await validate_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 400, detail="Incorrect email or password")
    elif not await user_crud.is_active(user):
        raise HTTPException(status_code = 400, detail="Inactive user")

    
    return await user_crud.update_access_token(user)


@router.get("/profile_user/")
async def profile_user(current_user: UsersAuth = Depends(get_current_active_user)):
    profile = await user_crud.get_user_profile(login = current_user.login)

    if not profile:
        raise HTTPException(status_code = 400, detail="profile does not exist")

    return profile

@router.put("/profile_user/update_profile_user")
async def update_profile_user(current_user:UserProfileUpdate =  Depends(get_current_active_user)):
    pass