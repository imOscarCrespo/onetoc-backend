from django.urls import path, re_path
from .views import (
    ActionListApiView,
    ClubListApiView,
    MatchListApiView,
    TeamListApiView
)

urlpatterns = [
    path('club', ClubListApiView.as_view()),
    path('team', TeamListApiView.as_view()),
    path('match', MatchListApiView.as_view()),
    path('action', ActionListApiView.as_view()),
]