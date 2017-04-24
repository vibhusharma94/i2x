from rest_framework import permissions as rest_permissions


class TeamMemberOnly(rest_permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user_is_team_member(request.user)
