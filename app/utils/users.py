from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException

from app.core.config import ALGORITHM, SECRET_KEY
from app.core.security import oauth2_scheme
from app.db.crud_user import user_crud
from app.core.security import pwd_context
from app.schemas.user import TokenPayload, User, UserInDB, UserProfileUpdate, UserRegistationRequest, UsersAuth


async def validate_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except:
        raise HTTPException(
            status_code=400,
            detail="Could not validate credentials",
        )
    user = await user_crud.get_user_by_login_auth(login=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(current_user:UsersAuth = Depends(get_current_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="Inactive user")
    return current_user