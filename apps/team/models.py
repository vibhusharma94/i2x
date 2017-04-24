from __future__ import unicode_literals
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Team(models.Model):
    """The Team model."""
    name = models.CharField(_('team name'), max_length=100)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Indicates whether team is active or not'))
    created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return self.name

    def add_member(self, user):
        if not isinstance(user, get_user_model()) or not user.is_active:
            member = None
        else:
            member, created = TeamMember.objects.get_or_create(team=self, user=user)
            if created:
                member.invitation_code = str(uuid.uuid4())
                member.save()
        return member

    def user_is_team_member(self, user):
        if not isinstance(user, get_user_model()) or not user.is_active:
            return False
        return self.members.all().filter(user=user).exists()


class TeamMember(models.Model):
    """The Team Member model."""
    team = models.ForeignKey(Team, related_name='members')
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    invitation_code = models.CharField(_('code'), max_length=255, blank=True)
    created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return "%s @ %s" % (self.user.get_full_name(), self.team.name)
