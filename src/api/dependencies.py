from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
import jwt

from exceptions import InvalidToken, NotActiveUser, NotSuperuser
from models.user import UserModel
from repositories.refresh_session import RefreshSessionRepository
from repositories.user import UserRepository
from services.auth import AuthService
from services.user import UserService
from utils.auth_utils import jwt_decode


def auth_service():
    return AuthService(UserRepository, RefreshSessionRepository)


def user_service():
    return UserService(UserRepository)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        print(scheme, param)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    access_token: str = Depends(oauth2_scheme),
    service: UserService = Depends(user_service),
) -> Optional[UserModel]:
    try:
        user = jwt_decode(access_token)
        user = await service.get_one_by_user_id(UUID(user.get("sub")))
        if user is None:
            raise InvalidToken
    except jwt.InvalidTokenError:
        raise InvalidToken
    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> Optional[UserModel]:
    if not current_user.is_active:
        raise NotActiveUser
    return current_user


async def get_current_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> Optional[UserModel]:
    if not current_user.is_superuser:
        raise NotSuperuser
    return current_user
