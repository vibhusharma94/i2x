import hashlib
import time
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Define the custom user class which can have additional attributes.
    """
    NAME_CHARACTER_LIMIT = {
        'FIRST_NAME': 55,
        'LAST_NAME': 55
    }
    FIELDS_CHARACTER_LIMIT = {
        'EMAIL_LIMIT': 255,
    }

    first_name = models.CharField(_('first name'), max_length=NAME_CHARACTER_LIMIT['FIRST_NAME'])
    last_name = models.CharField(_('last name'), max_length=NAME_CHARACTER_LIMIT['LAST_NAME'])
    email = models.EmailField(max_length=FIELDS_CHARACTER_LIMIT['EMAIL_LIMIT'], unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Admin access allowed?'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('User is active and is not Blocked?'))
    is_verified = models.BooleanField(_('verified'), default=False, help_text=_('User email is verified?'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def username(self):
        return self.get_username()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __unicode__(self):
        return self.email

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Always save the email in lowercase
        self.email = self.email.lower()
        super(User, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_account_activation_key(self):
        try:
            return self.email_verification
        except ObjectDoesNotExist:
            data = {'user': self, 'activation_key': str(uuid.uuid4())}
            return AccountActivation.objects.create(**data)


class CustomTokenManager(models.Manager):
    # Manager for CustomToken model
    def get_queryset(self):
        return super(CustomTokenManager, self).get_queryset().select_related(
            'user'
        )


class CustomToken(Token):
    """
    The authorization token model Override from the default Rest_framework's Token model
    """
    expiry_time = models.DateTimeField(default=timezone.now)
    refresh_token = models.CharField(max_length=40, blank=True, null=True)

    objects = CustomTokenManager()

    class Meta(Token.Meta):
        verbose_name = "API Authentication Token"
        verbose_name_plural = "API Authentication Tokens"

    def is_valid_token(self):
        return timezone.now() < self.expiry_time

    def get_epoch_expiry_time(self):
        return int(time.mktime(self.expiry_time.timetuple()))

    def validate_token(self, remember_me):
        self.expiry_time = timezone.now() + timedelta(hours=(settings.TOKEN_EXPIRY_TIME))
        self.save()

    def refresh_token_life(self):
        time_gap = timedelta(hours=settings.TOKEN_EXPIRY_TIME)
        self.expiry_time = timezone.now() + time_gap
        self.refresh_token = self.generate_key()
        self.save()

    def save(self, *args, **kwargs):
        if not self.refresh_token:
            self.refresh_token = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)


class PasswordResetManager(models.Manager):
    """ Password Reset Manager """

    def get_or_create_for_user(self, user):
        """ get or create password reset key for specified user """
        # support passing email address too
        if type(user) is unicode:
            user = User.objects.get(email=user)
        reset_key = hashlib.md5(user.email + str(user.id) + str(timezone.now())).hexdigest()
        password_reset = PasswordReset.objects.create(user=user, reset_key=reset_key)

        return password_reset


class PasswordReset(models.Model):
    """
    Password reset Key
    """
    user = models.ForeignKey(User, verbose_name=_("user"))

    reset_key = models.CharField(_("reset_key"), max_length=100, unique=True)
    created = models.DateTimeField(_("created at"), default=timezone.now)
    is_active = models.BooleanField(_("link still active"), default=True)

    objects = PasswordResetManager()

    class Meta:
        verbose_name = _('password reset')
        verbose_name_plural = _('password resets')

    def __unicode__(self):
        return "{} (key={})".format(self.user.email, self.reset_key)


class AccountActivation(models.Model):
    user = models.OneToOneField(User, related_name='email_verification')
    activation_key = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(_("created at"), default=timezone.now)
    is_active = models.BooleanField(_("link still active"), default=True)

    class Meta:
        verbose_name = _('email verification')
        verbose_name_plural = _('email verifications')

    def __unicode__(self):
        return "{} (key={})".format(self.user.email, self.activation_key)
