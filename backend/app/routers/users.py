from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.db.crud_user import user_crud
from app.core.data_for_openapi import ExampleSchemes
from app.utils.users import get_current_active_user, validate_password
from app.schemas.user import Password, Token, User, UserRegistationRequest, UsersAuth, UserProfileResponse

router = APIRouter(tags=["users"])

@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register_user(user_reg: UserRegistationRequest = Body(..., example=ExampleSchemes.register)):
    """ 
    Registration of users in the application: 

    - **login**: The unique identifier of the user by which he can log in or by email
    - **email**: 2 way to log in to the application
    - **password**: user password
    - **password_verification**: password confirmation

    Returns the data of the registered user:

    - **hashed_password**: hashed user password
    """    
    try:
        result = await user_crud.create_user(user_reg)
        await user_crud.create_user_token(user_reg)
        await user_crud.create_user_profile(user_reg)
    except:
        raise HTTPException(status_code = 400, detail="Such a user already exists")
    return result

@router.post("/log-in", response_model = Token, status_code = status.HTTP_200_OK)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ 
    Login (authorization) in the application: 

    - **username**: username or email of the user
    - **password**: user password

    Returns the jwt token and its type:
    
    - **access_token**: jwt authorization token
    - **token_type**: type token
    """    
    user = await user_crud.get_user_by_email(email = form_data.username)
    if not user:
        user = await user_crud.get_user_by_login(login = form_data.username)
        if not user:
            raise HTTPException(status_code = 400, detail="Incorrect email or password")

    if not await validate_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 400, detail="Incorrect email or password")
    elif not await user_crud.is_active(user):
        raise HTTPException(status_code = 400, detail="Inactive user")

    return await user_crud.update_access_token(user)


@router.get("/profile-user", response_model = UserProfileResponse, status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.profile_user 
 }}}})
async def profile_user(current_user: UsersAuth = Depends(get_current_active_user)):
    """ 
    Viewing user information (only for an authorized user): 


    Returns user information:
    
    - **login**: The unique identifier of the user by which he can log in or by email
    - **email**: 2 way to log in to the application
    - **first_name**: User name
    - **last_name**: User's last name
    - **registered**: account registration date
    """     
    profile = await user_crud.get_user_profile(login = current_user.login)
    if not profile:
        raise HTTPException(status_code = 400, detail="profile does not exist")
    
    return profile

@router.put("/profile-user/update-profile-user", status_code = status.HTTP_200_OK)
async def update_profile_user(last_name: str, first_name: str, current_user:User =  Depends(get_current_active_user)):
    """ 
    Updating user information (authorized user only): 

    - **first_name**: User name
    - **last_name**: User's last name
    """

    return await user_crud.update_user_profile(last_name, first_name, current_user)

@router.post("/recover-password/{email_or_login}", status_code = status.HTTP_200_OK)
async def resert_password(email_or_login: str, password: Password):
    """ 
    Password reset and update:

    - **emai_or_login**: email or login of the account we want to change the password for
    - **password**: new user password
    - **password_verification**: password confirmation
    """    
    user = await user_crud.get_user_by_email(email_or_login)
    if not user:
        user = await user_crud.get_user_by_login(email_or_login)
        if not user:
            raise HTTPException(status_code = 404, detail="user does not found")

    return await user_crud.recover_password(user, password)

@router.delete("/profile-user/delete-user", status_code = status.HTTP_200_OK)
async def delete_user(current_user: User =  Depends(get_current_active_user)):
    """ 
    Deleting a user and all information related to him
    """     
    return await user_crud.delete_user(current_user)