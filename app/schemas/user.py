from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: EmailStr
    login: str

class UserRegistationRequest(UserBase):
    password: str
    password_ver: str

class UserInDB(UserBase):
    hashed_password: str