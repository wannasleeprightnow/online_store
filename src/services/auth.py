from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4


from exceptions import (
    InvalidToken,
    NotValidName,
    NotValidPassword,
    NotValidUsername,
    TokenExpired,
    UserAlreadyExists,
)
from models.refresh_session import RefreshSessionModel
from models.user import UserModel
from repositories.refresh_session import RefreshSessionRepository
from repositories.user import UserRepository
from schemas.token import Token
from schemas.user import UserRegister
from settings import ValidatorSettings
from utils.auth_utils import (
    hash_password,
    is_valid_password,
    jwt_encode,
)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_session_repository: RefreshSessionRepository,
    ) -> None:
        self.user_repository: UserRepository = user_repository()
        self.refresh_session_repository: RefreshSessionRepository = (
            refresh_session_repository()
        )

    async def register(self, user: UserRegister) -> UserModel:

        if (
            await self.user_repository.get_one_by_username(user.username)
            is not None
        ):
            raise UserAlreadyExists

        if not ValidatorSettings.USERNAME_VALIDATE.match(user.username):
            raise NotValidUsername
        if not ValidatorSettings.PASSWORD_VALIDATE.match(user.password):
            raise NotValidPassword
        if not ValidatorSettings.NAME_VALIDATE.match(user.name):
            raise NotValidName

        user.password = hash_password(user.password)
        user = await self.user_repository.insert_one(user.model_dump())

        return user

    async def authenticate(
        self, username: Optional[str], password: Optional[str]
    ) -> Optional[UserModel]:

        user = await self.user_repository.get_one_by_username(username.strip())

        if user is not None and is_valid_password(
            password.strip(), user.password
        ):
            return user

        return None

    async def create_token(self, user_id: uuid4) -> Token:
        access_token = jwt_encode(payload={"sub": str(user_id)})
        refresh_token: RefreshSessionModel = (
            await self.refresh_session_repository.insert_one(
                {"token": uuid4(), "user_id": user_id}
            )
        )
        return Token(
            access_token=access_token, refresh_token=refresh_token.token
        )

    async def refresh_token(self, refresh_token: str) -> Optional[Token]:
        if refresh_token is None:
            raise InvalidToken

        refresh_session = (
            await self.refresh_session_repository.get_session_by_token(
                UUID(refresh_token.strip())
            )
        )
        if refresh_session is None:
            raise InvalidToken

        user = await self.user_repository.get_one_by_user_id(
            refresh_session.user_id
        )
        if user is None:
            raise InvalidToken

        session_expire_time = refresh_session.created_at + timedelta(
            seconds=refresh_session.expire_time_seconds
        )
        if datetime.now(timezone.utc) >= session_expire_time:
            await self.refresh_session_repository.delete_session_by_id(
                refresh_session.id
            )
            raise TokenExpired

        access_token = jwt_encode(payload={"sub": str(user.id)})
        refresh_token: RefreshSessionModel = (
            await self.refresh_session_repository.update_session_by_id(
                uuid4(), user.id
            )
        )
        return Token(
            access_token=access_token, refresh_token=refresh_token.token
        )

    async def logout(self, refresh_token: UUID) -> None:
        if await self.refresh_session_repository.get_session_by_token(
            refresh_token
        ):
            await self.refresh_session_repository.delete_session_by_token(
                refresh_token
            )

    async def abort_all_sessions(self, user_id: UUID):
        if await self.refresh_session_repository.get_session_by_user_id(
            user_id
        ):
            await self.refresh_session_repository.delete_session_by_token(
                user_id
            )
