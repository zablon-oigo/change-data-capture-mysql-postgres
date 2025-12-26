from fastapi import APIRouter, Depends, status, HTTPException,BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone

from src import mail
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from .schemas import PasswordResetConfirmModel, PasswordResetRequestModel, UserCreateModel, UserLoginModel, UserModel, UserBooksModel
from .services import UserService
from .utils import verify_password, create_access_token, generate_password_hash
from src.celery import send_email  
from src.mail import create_message
from src.auth.schemas import EmailModel,SignupResponseModel
from src.errors import UserNotFound, UserAlreadyExists
from src.config import Config
from src.mail import mail, create_message

from src.auth.utils import (
    create_url_safe_token,
    decode_url_safe_token,
)

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)

role_checker = RoleChecker(["admin","user"])
admin_checker = RoleChecker(["admin"])
auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY_DAYS = 7  

refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()



@auth_router.post("/signup", response_model=SignupResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email.lower()

    if await user_service.user_exists(email, session):
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html = f"""
    <h1>Welcome to {Config.APP_NAME}</h1>
    <p>Hi {new_user.username},</p>
    <p>Thank you for registering at {Config.APP_NAME}.</p>
    <p>Click the link below to verify your email:</p>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    <p>If you did not sign up, you can safely ignore this email.</p>
    """
    send_email.delay([email], "Verify Your Email", html)

    return {
        "message": "Account created,Check your email to verify your account.",
        "user": new_user,
    }


@auth_router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    if not token_data or "email" not in token_data:
        return JSONResponse(
            content={"message": "Invalid or expired verification link"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user_email = token_data["email"].lower()
    user = await user_service.get_user_by_email(user_email, session)

    if not user:
        raise UserNotFound()

    if user.is_verified:
        return JSONResponse(
            content={"message": "Account already verified"},
            status_code=status.HTTP_200_OK,
        )
    await user_service.update_user(user, {"is_verified": True}, session)

    return JSONResponse(
        content={"message": "Account verified successfully.You can now log in."},
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/me", response_model=UserBooksModel)
async def me(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user



@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_users(
    login_data: UserLoginModel, 
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email.lower()
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)}
    )
    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)},
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "uid": str(user.uid)},
        }
    )


@auth_router.get("/refresh_token", status_code=status.HTTP_200_OK)
async def get_new_access_token(
    token_details: dict = Depends(refresh_token_bearer)
):
    expiry_timestamp = token_details.get("exp")
    if not expiry_timestamp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    token_expiry = datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc)
    now_utc = datetime.now(timezone.utc)

    if token_expiry < now_utc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or invalid"
        )

    new_access_token = create_access_token(user_data=token_details["user"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": new_access_token}
    )



@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token_data: dict = Depends(access_token_bearer)):
    jti = token_data['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logged out successfully"}
    )

@auth_router.get("/all-users", response_model=list[UserModel])
async def get_all_users(
    _: bool = Depends(admin_checker), 
    session: AsyncSession = Depends(get_session)
):
    users = await user_service.get_all_users(session)
    return users or []


@auth_router.delete("/user/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_uid: str, 
    _: bool = Depends(admin_checker), 
    session: AsyncSession = Depends(get_session)
):
    deleted = await user_service.delete_user(user_uid, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

