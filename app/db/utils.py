
from app.db.base import database
from app.models.user import users
from app.core.security import get_hash_password
from app.schemas.user import UserRegistationRequest


async def create_user(user: UserRegistationRequest ):
    query = users.insert().values(
        login=user.login, email=user.email, hashed_password=get_hash_password(user.password)
    )
    result = await database.execute(query)
    return result