from django.urls import path, re_path
from .views import (
    ActionListApiView,
    ClubListApiView,
    EventListApiView,
    MatchListApiView,
    TabListApiView,
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
    path('tab', TabListApiView.as_view()),
    path('event', EventListApiView.as_view()),
    re_path('action/(?P<id>\d+)', ActionListApiView.as_view(), name='action'),
    re_path('match/(?P<id>\d+)', MatchListApiView.as_view(), name='match_by_id'),
    re_path('event/(?P<id>\d+)', EventListApiView.as_view(), name='event_by_match_id'),
    path('timeline', TimelineListApiView.as_view()),
    path('csrf', CsrfApiView.as_view()),
    path('logout', LogoutView.as_view())
]