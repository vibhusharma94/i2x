from django.conf.urls import include, url
from rest_framework import routers
from apps.team import views as team_views


team_router = routers.SimpleRouter()
team_router.register(r'team', team_views.TeamViewSet, 'team')

urlpatterns = [
    url(r'^', include(team_router.urls)),
]
