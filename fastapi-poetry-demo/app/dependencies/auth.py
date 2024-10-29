from datetime import datetime, timezone, timedelta
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import bcrypt

from ..configs.auth import get_auth_settings
from .exceptions import HTTP_401_UNAUTHORIZED

auth_settings = get_auth_settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def create_access_token(*, data: dict) -> str:
    """创建JWT令牌

    :param data:
    :return:
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, auth_settings.AUTH_SECRET_KEY, algorithm=auth_settings.AUTH_ALGORITHM
    )
    return encoded_jwt


async def extract_access_token(token: str = Depends(oauth2_scheme)):
    """从JWT令牌中解析出用户信息

    :param token: JWT令牌
    :return: 用户信息
    """

    try:
        payload = jwt.decode(
            token,
            auth_settings.AUTH_SECRET_KEY,
            algorithms=[auth_settings.AUTH_ALGORITHM],
        )
        return payload
        # user = await User.get_active_user(account=payload.get("account"))
    except jwt.PyJWTError:
        raise HTTP_401_UNAUTHORIZED
    # if not user:
    #     raise HTTP_401_UNAUTHORIZED
    # return user


