from django.test import TestCase

from apps.userauth.tests.factories import UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_create_account_activation_key(self):
        email_verification = self.user.create_account_activation_key()
        self.assertEqual(email_verification, self.user.email_verification)
