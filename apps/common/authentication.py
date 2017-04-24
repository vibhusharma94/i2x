from django.contrib.auth import get_user_model

from rest_framework import (
    authentication as rest_authentication,
    exceptions as rest_exceptions
)

from apps.common import exceptions as common_exceptions
from apps.userauth import models as userauth_models


class CustomTokenAuthentication(rest_authentication.TokenAuthentication):
    """
    Custom token based authentication , Override from the basic rest_authentication.TokenAuthentication Class
    Token validation condition is added to the default authenticate_credentials function
    Default Token model is also changed to the CustomToken Model
    """
    model = userauth_models.CustomToken

    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise rest_exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise rest_exceptions.AuthenticationFailed('User inactive or deleted')

        if not token.is_valid_token():
            raise common_exceptions.TokenExpired('Token expired')

        return get_user_model().objects.get(pk=token.user_id), token
