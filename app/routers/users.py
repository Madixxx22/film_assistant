from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_hash_password
from app.models.base import get_db
from app.models.crud import create_user

from app.schemas.user import UserCreate, UserRegistationRequest

router = APIRouter()

@router.post("/register")
async def register_user(user_reg: UserRegistationRequest, db: Session = Depends(get_db)):
    hash_password = get_hash_password(user_reg.password)
    user_create = UserCreate(email = user_reg.email, hash_password = hash_password)
    create_user(db, user_create)

    return {"Успех": "Успешный"}