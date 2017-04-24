from django.test import TestCase

from apps.userauth.utils import validate_user_auth_token
from apps.userauth.tests.factories import UserFactory
from apps.userauth import models as userauth_models


class AuthTokenTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_validate_user_auth_token(self):
        token = validate_user_auth_token(self.user)
        current_token = userauth_models.CustomToken.objects.filter(user=self.user).last()
        self.assertEqual(token, current_token)
