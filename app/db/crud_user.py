from datetime import datetime, timedelta
from pydantic import EmailStr
from app.core.security import create_access_token, get_hash_password

from app.schemas.user import User, UserInDB, UserProfileResponce, UserRegistationRequest, UsersAuth, Token
from .base import database
from app.models.user import users, users_authentication, user_profile

class UserCRUD():
    async def get_user_by_email(self, email: EmailStr) -> UserInDB:
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)
    
    async def get_user_by_login(self, login: str) -> UserInDB:
        query = users.select().where(users.c.login == login)
        return await database.fetch_one(query)

    async def get_user_by_login_auth(self, login: str) -> UsersAuth:
        query = users_authentication.select().where(users_authentication.c.login == login)
        return await database.fetch_one(query)
    
    async def get_user_profile(self, login: str) -> UserProfileResponce:
        query = user_profile.select().where(user_profile.c.login == login)
        return await database.fetch_one(query)
    
    async def create_user(self, user: UserRegistationRequest):
        query = users.insert().values(
            login=user.login, email=user.email, hashed_password=get_hash_password(user.password)
        )
        return await database.execute(query)

    async def create_user_token(self, user: User):
        auth_code = create_access_token(data = {"sub": user.login})
        query = users_authentication.insert().values(
            login=user.login, generated_timestamp = datetime.now() + timedelta(weeks=2),
            auth_code=auth_code, is_used = True
        )
        return await database.execute(query)
    
    async def is_active(self, user: User):
        query = users_authentication.select(users_authentication.c.is_used).where(
            users_authentication.c.login == user.login
        )
        return database.fetch_one(query)
    
    async def create_user_profile(self, user: User):
        query = user_profile.insert().values(login=user.login, registered=datetime.now())
        return await database.execute(query)
    
    async def update_access_token(self, user: User):
        auth_code=create_access_token(data = {"sub": user.login})
        query = users_authentication.update().where(
            users_authentication.c.login == user.login).values(
                auth_code=auth_code, generated_timestamp = datetime.now() + timedelta(weeks=2)
            )
        await database.execute(query)
        return Token(access_token = auth_code)

user_crud = UserCRUD()