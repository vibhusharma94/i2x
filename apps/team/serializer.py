from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers as rest_serializers

from apps.team import models as team_models
from apps.common import base_serializers


class TeamSerializer(base_serializers.BaseModelSerializer):

    class Meta:
        model = team_models.Team
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            team_models.TeamMember.objects.get(user=user)
        except team_models.TeamMember.DoesNotExist:
            team = team_models.Team.objects.create(**validated_data)
            team.add_member(user)
            return team

        raise rest_serializers.ValidationError(_("Unable to create team, User is already a team member"))


class TeamMemberSerializer(base_serializers.BaseModelSerializer):

    class Meta:
        model = team_models.TeamMember
        fields = "__all__"
