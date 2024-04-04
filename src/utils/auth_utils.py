from datetime import datetime, timedelta

import bcrypt
import jwt

from settings import AuthJWTSettings


def jwt_encode(
    payload: dict,
    private_key: str = AuthJWTSettings.PRIVATE_KEY.read_text(),
    expire_time_seconds: int = AuthJWTSettings.ACCESS_TOKEN_EXPIRE_SECONDS,
    algorithm: str = AuthJWTSettings.ALGORITHM,
) -> str:
    expire_time = datetime.utcnow() + timedelta(seconds=expire_time_seconds)
    payload.update(exp=expire_time)

    encoded_jwt_token = jwt.encode(
        payload=payload, key=private_key, algorithm=algorithm
    )
    return f"Bearer {encoded_jwt_token}"


def jwt_decode(
    token: str,
    public_key: str = AuthJWTSettings.PUBLIC_KEY.read_text(),
    algorihtm: str = AuthJWTSettings.ALGORITHM,
) -> dict:
    decoded_jwt_token = jwt.decode(
        jwt=token, key=public_key, algorihtms=[algorihtm]
    )
    return decoded_jwt_token


def is_valid_password(unhashed_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(unhashed_password.encode(), hashed_password)


def hash_password(unhashed_password: str) -> bytes:
    return bcrypt.hashpw(unhashed_password.encode(), bcrypt.gensalt())
