from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

from app.db.base import database
from app.models.user import users, users_authentication
from app.core.security import create_access_token, get_hash_password, pwd_context
from app.schemas.user import User, UserInDB, UserRegistationRequest


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

async def create_user_token(user):
    auth_code=create_access_token(data = {"sub": user.login})
    query = (
        users_authentication.insert()
        .values(login=user.login, generated_timestamp=datetime.now() + timedelta(weeks=2),
                auth_code=auth_code, is_used=True)
    )
    return  await database.fetch_one(query)

async def is_active(user: UserInDB):
    query = users_authentication.select(users_authentication.c.is_used).where(
        users_authentication.c.login == user.login)
    return await database.fetch_one(query)