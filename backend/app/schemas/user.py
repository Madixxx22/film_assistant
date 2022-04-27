import datetime
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: EmailStr
    login: str

class Password(BaseModel):
    password: str
    password_verification: str
    #checking for matching passwords
    @validator("password_verification")
    def password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v

class UserRegistationRequest(UserBase, Password):
    pass

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    pass

class UserProfileUpdate(UserBase):
    last_name: str = None
    first_name: str = None
    
class UserProfileResponse(UserProfileUpdate):
    registered: datetime.date

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsersAuth(BaseModel):
    login: str
    generated_timestamp: datetime.date
    auth_code: str
    is_used: bool


class TokenPayload(BaseModel):
    sub: str | None = None