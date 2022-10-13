from django.urls import path, re_path
from .views import (
    ActionListApiView,
    ClubListApiView,
    MatchListApiView,
    TeamListApiView,
    TimelineListApiView,
    CsrfApiView,
    LogoutView
)

urlpatterns = [
    path('club', ClubListApiView.as_view()),
    path('team', TeamListApiView.as_view()),
    path('match', MatchListApiView.as_view()),
    path('action', ActionListApiView.as_view()),
    path('timeline', TimelineListApiView.as_view()),
    path('csrf', CsrfApiView.as_view()),
    path('logout', LogoutView.as_view())
]