from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, HTTPException
from app.core.config import ALGORITHM, SECRET_KEY
from app.db.base import database
from app.core.security import oauth2_scheme
from app.models.user import users, users_authentication, user_profile
from app.core.security import create_access_token, get_hash_password, pwd_context
from app.schemas.user import TokenPayload, User, UserInDB, UserInfoUpdate, UserRegistationRequest


async def get(id):
    query = users_authentication.select().where(users_authentication.c.login == id)
    return await database.fetch_one(query)

async def create_user(user: UserRegistationRequest ):
    query = users.insert().values(
        login=user.login, email=user.email, hashed_password=get_hash_password(user.password)
    )
    result = await database.execute(query)
    return result

async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)

async def validate_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

async def create_user_token(user: User):
    auth_code=create_access_token(data = {"sub": user.login})
    query = (
        users_authentication.insert()
        .values(login=user.login, generated_timestamp=datetime.now() + timedelta(weeks=2),
                auth_code=auth_code, is_used=True)
    )
    return  await database.fetch_one(query)

async def is_active(user: User):
    query = users_authentication.select(users_authentication.c.is_used).where(
        users_authentication.c.login == user.login)
    return await database.fetch_one(query)

async def create_user_info(user: User):
    query = user_profile.insert().values(login=user.login, registered=datetime.now())
    return await database.fetch_one(query)

async def update_user_info():
    pass

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
    user = get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(current_user:UserInfoUpdate = Depends(get_current_user)):
    if not is_active(current_user):
        raise HTTPException(status_code = 400, detail="Inactive user")
    return current_user

async def update_access_token(user: User):
    auth_code=create_access_token(data = {"sub": user.login})
    query = users_authentication.update().where(
        users_authentication.c.login == user.login).values(
        auth_code=auth_code, generated_timestamp = datetime.now() + timedelta(weeks=2), is_used = True)
    return await database.fetch_one(query)