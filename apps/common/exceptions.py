from rest_framework import (
    exceptions as rest_exceptions
)
from rest_framework import status

from apps.common import status as common_status


class TokenExpired(rest_exceptions.APIException):
    status_code = common_status.HTTP_SESSION_EXPIRED
    default_detail = 'Token Expired'


class InvalidRefreshToken(rest_exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid Refresh Token'
