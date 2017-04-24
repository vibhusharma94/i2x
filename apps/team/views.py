import logging

from rest_framework import (
    response as rest_response,
    exceptions as rest_exceptions,
    viewsets as rest_viewsets,
)
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from apps.team import serializer as team_serializer
from apps.team import models as team_models
from apps.team import permissions as team_permissions

logger = __name__
log = logging.getLogger(logger)


class TeamViewSet(rest_viewsets.GenericViewSet):
    """
    Team API ViewSet
    """
    permission_classes = (IsAuthenticated,)
    queryset = team_models.Team.objects.all()
    serializer_class = team_serializer.TeamSerializer

    def create(self, request):
        # create team if user doesn't have a team already
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return rest_response.Response(serializer.data)
        raise rest_exceptions.ParseError(serializer.errors)

    @detail_route(methods=['get'], url_path='members', permission_classes=[team_permissions.TeamMemberOnly])
    def members(self, request, pk):
        team = self.get_object()
        page = self.paginate_queryset(team.members.all())
        serializer = team_serializer.TeamMemberSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
