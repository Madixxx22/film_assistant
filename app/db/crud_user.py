import sqlalchemy
from pydantic import EmailStr
from datetime import datetime, timedelta, date

from .base import database
from app.core.security import create_access_token, get_hash_password
from app.models.user import users, users_authentication, user_profile
from app.schemas.user import Password, User, UserInDB, UserProfileResponse, UserRegistationRequest, UsersAuth, UserRegistationRequest, UsersAuth, Token

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
    
    async def get_user_profile(self, login: str) -> UserProfileResponse:
        query = (sqlalchemy.select(
            [users.c.email, users.c.login, user_profile.c.last_name,
            user_profile.c.first_name, user_profile.c.registered]
            ).select_from(user_profile.join(users)).where(user_profile.c.login == login))
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
        await database.execute(query)
    
    async def is_active(self, user: User) -> bool:
        query = users_authentication.select(users_authentication.c.is_used).where(
            users_authentication.c.login == user.login
        )
        return await database.fetch_one(query)
    
    async def create_user_profile(self, user: User):
        query = user_profile.insert().values(login=user.login, registered=date.today())
        return await database.execute(query)
    
    async def update_access_token(self, user: User):
        auth_code=create_access_token(data = {"sub": user.login})
        query = users_authentication.update().where(
            users_authentication.c.login == user.login).values(
                auth_code=auth_code, generated_timestamp = datetime.now() + timedelta(weeks=2)
            )
        await database.execute(query)
        return Token(access_token = auth_code)

    async def update_user_profile(self, last_name: str, first_name: str, current_user: User):
        query = user_profile.update().where(
            user_profile.c.login == current_user.login).values(
                last_name = last_name, first_name = first_name
            )
        return await database.execute(query)

    async def recover_password(self, user: UserInDB, password: Password):
        query = users.update().where(
            users.c.login == user.login).values(
            hashed_password = get_hash_password(password.password))
        return await database.execute(query)

    async def delete_user(self, user):
        query = users.delete().where(users.c.login == user.login)
        return await database.execute(query)

user_crud = UserCRUD()