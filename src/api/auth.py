from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import auth_service
from exceptions import InvalidCredentials
from settings import AuthJWTSettings
from services.auth import AuthService
from schemas.token import Token
from schemas.user import UserBase, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserBase)
async def register(
    user: UserRegister, service: AuthService = Depends(auth_service)
):
    return await service.register(user)


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(auth_service),
):
    user = await service.authenticate(
        credentials.username, credentials.password
    )
    if not user:
        raise InvalidCredentials
    token = await service.create_token(user.id)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=AuthJWTSettings.ACCESS_TOKEN_EXPIRE_SECONDS,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=AuthJWTSettings.REFRESH_TOKEN_EXPIRE_SECONDS,
        httponly=True,
    )
    return token


@router.post("/refresh", response_model=Token)
async def refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(auth_service),
):
    new_token = await service.refresh_token(
        request.cookies.get("refresh_token")
    )
    response.set_cookie(
        "access_token",
        new_token.access_token,
        max_age=AuthJWTSettings.ACCESS_TOKEN_EXPIRE_SECONDS,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        new_token.refresh_token,
        max_age=AuthJWTSettings.REFRESH_TOKEN_EXPIRE_SECONDS,
        httponly=True,
    )
    return new_token
