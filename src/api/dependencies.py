from repositories.refresh_session import RefreshSessionRepository
from repositories.user import UserRepository
from services.auth import AuthService
from services.user import UserService


def auth_service():
    return AuthService(UserRepository, RefreshSessionRepository)


def user_service():
    return UserService(UserRepository)
