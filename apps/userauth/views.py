import logging

from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import (
    response as rest_response,
    exceptions as rest_exceptions,
    generics as rest_generics,
    views as rest_views,
)
from rest_framework.authtoken import serializers as rest_authtoken_serializers

from apps.common import base_serializers as common_serializer
from apps.userauth import serializer as userauth_serializer
from apps.userauth import models as userauth_models
from apps.userauth import utils as userauth_utils


logger = __name__
log = logging.getLogger(logger)


class SignupView(rest_generics.GenericAPIView):
    """
    Signup API View
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = userauth_serializer.UserSerializer

    def post(self, request):
        data = request.data.copy()
        data['invitation_code'] = self.request.query_params.get('invite_code')
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return rest_response.Response(serializer.data)
        raise rest_exceptions.ParseError(serializer.errors)


class LoginView(rest_generics.GenericAPIView):
    """
    Customized Auth Token Authentication API View, So it returns User data as well
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = rest_authtoken_serializers.AuthTokenSerializer

    def post(self, request):
        """
        Post method over-ridden to return User data along with auth Token if authenticated
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.is_verified:
                return self.permission_denied()
            token = userauth_utils.validate_user_auth_token(user)
            return rest_response.Response(userauth_serializer.UserSerializer(
                user, context={'token': token}
            ).data)
        raise rest_exceptions.ParseError(serializer.errors)

    def permission_denied(self):
        raise rest_exceptions.PermissionDenied(
            _("Verify your email in order to login"))


class LogoutView(rest_views.APIView):
    """
    Logout the user from server by invalidating the token
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            # Only if User is logged in
            try:
                token_obj = userauth_models.CustomToken.objects.get(user=request.user)
            except userauth_models.CustomToken.DoesNotExist:
                log.info("CustomToken object not found for user", request.user.email)
            else:
                if token_obj.is_valid_token():
                    # Invalidate the token
                    token_obj.delete()
        return rest_response.Response(userauth_serializer.LogoutSerializer().data)


class RefreshTokenView(rest_views.APIView):
    """
    View to refresh token
    """
    permission_classes = ()
    serializer_class = userauth_serializer.RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return rest_response.Response(serializer.data)
        raise rest_exceptions.ParseError(serializer.errors)


class PasswordResetRequestKey(rest_generics.GenericAPIView):
    """
    Sends an email to the user email address with a link to reset his password.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = userauth_serializer.ResetPasswordSerializer
    model = userauth_models.PasswordReset

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # send reset password email to user, Logic not implemented
            message = _(u'We just sent you the link with which you will '
                        u'able to reset your password at %s') % request.data.get('email')

            return rest_response.Response(common_serializer.CustomMessageSerializer(custom_message=message).data)
        raise rest_exceptions.ParseError(serializer.errors)

    def permission_denied(self, request):
        raise rest_exceptions.PermissionDenied(_("You can't reset your password if you are already authenticated"))


class PasswordResetFromKey(rest_generics.GenericAPIView):
    """
    Reset password from key.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = userauth_serializer.ResetPasswordKeySerializer

    def post(self, request, key):
        try:
            expiry_date = timezone.now() - timedelta(settings.RESET_PASSWORD_LINK_EXPIRE)
            password_reset = userauth_models.PasswordReset.objects.get(reset_key=key,
                                                                       created__gt=expiry_date,
                                                                       is_active=True)
        except (ValueError, userauth_models.PasswordReset.DoesNotExist, AttributeError):
            raise rest_exceptions.NotFound(_('Key not found.'))

        serializer = userauth_serializer.ResetPasswordKeySerializer(
            data=request.data,
            instance=password_reset
        )
        if serializer.is_valid():
            serializer.save()
            message = _(u'Password successfully reset.')
            return rest_response.Response(common_serializer.CustomMessageSerializer(custom_message=message).data)
        raise rest_exceptions.ParseError(serializer.errors)

    def permission_denied(self, request):
        raise rest_exceptions.PermissionDenied(
            _("You can't reset your password if you are already authenticated"))


class EmailVerificationKey(rest_generics.GenericAPIView):
    """
    Email verification key.
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, key):
        try:
            email_verification = userauth_models.AccountActivation.objects.get(activation_key=key,
                                                                               is_active=True)
        except userauth_models.AccountActivation.DoesNotExist:
            raise rest_exceptions.NotFound(_('Key not found.'))

        user = email_verification.user
        user.is_verified = True
        user.save()
        email_verification.is_active = False
        email_verification.save()

        message = _(u'Account successfully verified.')
        return rest_response.Response(common_serializer.CustomMessageSerializer(custom_message=message).data)
