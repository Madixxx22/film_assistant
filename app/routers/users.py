from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.utils import create_user
from app.schemas.user import UserInDB, UserRegistationRequest

router = APIRouter()

@router.post("/register")
async def register_user(user_reg: UserRegistationRequest):
    result = await create_user(user_reg)

    return result