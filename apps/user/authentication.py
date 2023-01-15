import enum
from datetime import datetime, timedelta

import jwt

from apps.user.queries import get_user_obj, check_user_exists
from apps.utils.exceptions import AuthenticationError
from prj.settings import SECRET_KEY, ACCESS_TOKEN_EXP, REFRESH_TOKEN_EXP, logger


class TokenType(enum.Enum):
    ACCESS = "acc"
    REFRESH = "ref"


def get_login_info(user_id: str) -> dict:
    return {
        "access_token": generate_access_token(user_id),
        "refresh_token": generate_refresh_token(user_id)
    }


def generate_access_token(user_id):
    payload = {
        "uid": user_id,
        "type": TokenType.ACCESS.value,
        "exp": datetime.now() + timedelta(**ACCESS_TOKEN_EXP)
    }
    return jwt_encode(payload)


def generate_refresh_token(user_id):
    payload = {
        "uid": user_id,
        "type": TokenType.REFRESH.value,
        "exp": datetime.now() + timedelta(**REFRESH_TOKEN_EXP)
    }
    return jwt_encode(payload)


def jwt_encode(payload):
    """
    document:
        https://pyjwt.readthedocs.io/en/latest/
    """
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def jwt_decode(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


class TokenValidator:
    token_type = None

    def get_token_payload(self, token):
        if token:
            try:
                return jwt_decode(token)
            except Exception as error:
                logger.error(f"{type(error)}: {str(error)}")
        raise AuthenticationError

    def check_token_type(self, payload):
        token_type = payload.get("type")
        if token_type and token_type == self.token_type:
            return
        raise AuthenticationError

    def get_user_id_from_payload(self, payload):
        user_id = payload.get('uid')
        if user_id and check_user_exists(user_id):
            return user_id
        raise AuthenticationError

    def get_user_obj(self, payload):
        user_id = payload.get('uid')
        if user_id:
            user = get_user_obj(user_id)
            if user:
                return user
        raise AuthenticationError


class JWTAuthentication(TokenValidator):
    token_type = TokenType.ACCESS.value

    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        token_payload = self.get_token_payload(access_token)
        self.check_token_type(token_payload)
        return (self.get_user_obj(token_payload), access_token)
