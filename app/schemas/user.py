from pydantic import BaseModel, EmailStr, validator

class UserRegistationRequest(BaseModel):
    email: EmailStr
    password: str
    password_ver: str

class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str