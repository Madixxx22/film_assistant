import datetime
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: EmailStr
    login: str

class UserRegistationRequest(UserBase):
    password: str
    password_verification: str
    @validator("password_verification")
    def password_match(cls, v, values):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    pass

class UserInfoUpdate(UserBase):
    last_name: str
    first_name: str
    
class UserInfoResponce(UserInfoUpdate):
    registered_date: datetime.datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"