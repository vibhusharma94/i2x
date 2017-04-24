from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers as rest_serializers

from apps.userauth import (
    utils as userauth_utils,
    models as userauth_models
)
from apps.common import base_serializers
from apps.common import exceptions as common_exceptions
from apps.team import models as team_models


class UserSerializer(base_serializers.BaseModelSerializer):

    invitation_code = rest_serializers.CharField(max_length=500, required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        exclude = ('id', 'is_superuser', 'groups', 'user_permissions', 'date_joined', 'is_staff', 'is_active',
                   'last_login', 'updated_at')

        extra_kwargs = {
            'password': {'write_only': True},
            'invitation_code': {'write_only': True}
        }

    def to_representation(self, data):
        data = super(UserSerializer, self).to_representation(data)
        data = self.update_data(data)
        return data

    def update_data(self, result):
        token = self.context.get('token', None)
        if token:
            result.update(userauth_utils.get_token_dict(token))
        return result

    def create(self, validated_data):
        if 'invitation_code' in validated_data:
            invitation_code = validated_data.pop('invitation_code')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        self.assign_team(user, invitation_code)
        user.create_account_activation_key()
        # send verification email to user, logic not implemented. Look into common.mailers.py
        return user

    def assign_team(self, user, code):
        try:
            member = team_models.TeamMember.objects.get(invitation_code=code)
            member.team.add_member(user)
        except team_models.TeamMember.DoesNotExist:
            pass


class RefreshTokenSerializer(base_serializers.BaseAPISerializer):
    """
    Return the token related details on refresh token
    """
    refresh_token = rest_serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        try:
            token = userauth_models.CustomToken.objects.get(refresh_token=refresh_token)
            token.refresh_token_life()
            attrs['token'] = token
        except userauth_models.CustomToken.DoesNotExist:
            raise common_exceptions.InvalidRefreshToken
        return attrs

    def to_representation(self, instance):
        token = instance['token']
        token_dict = userauth_utils.get_token_dict(token)
        data = super(RefreshTokenSerializer, self).to_representation(instance)
        data.update(token_dict)
        return data


class LogoutSerializer(base_serializers.BaseAPISerializer):
    def to_representation(self, instance):
        return super(LogoutSerializer, self).to_representation(instance)


class ResetPasswordSerializer(base_serializers.BaseAPISerializer):

    email = rest_serializers.EmailField(required=True)

    class Meta:
        model = userauth_models.PasswordReset

    def validate_email(self, value):
        """
        Add Case-insensitive unique validation for email
        """
        if get_user_model().objects.filter(email__iexact=value, is_active=True).count() == 0:
            raise rest_serializers.ValidationError(_("Email address not verified for any user account"))
        return value

    def create(self, validated_data):
        """
        create password reset for user
        """
        email = validated_data.get('email', None)
        password_reset = userauth_models.PasswordReset.objects.get_or_create_for_user(email)
        return password_reset


class ResetPasswordKeySerializer(base_serializers.BaseAPISerializer):

    password = rest_serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        user = instance.user
        password = validated_data.get('password', None)
        user.set_password(password)
        user.save()
        # mark password reset object as reset
        instance.reset = True
        instance.is_active = False
        instance.save()
        return instance

