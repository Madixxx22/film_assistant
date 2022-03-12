from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_hash_password

from app.schemas.user import UserCreate


async def create_user(db: Session, user: UserCreate ):
    db_user = User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user