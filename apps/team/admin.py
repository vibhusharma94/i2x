from django.contrib import admin
from apps.team import models as team_models


class TeamMemberAdmin(admin.StackedInline):
    model = team_models.TeamMember


class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberAdmin]
    list_display = ['name', 'created']

admin.site.register(team_models.Team, TeamAdmin)
