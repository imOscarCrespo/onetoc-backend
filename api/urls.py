from django.urls import path, re_path
from .views import (
    ActionListApiView,
    ClubListApiView,
    EventListApiView,
    MatchInfoListApiView,
    MatchListApiView,
    PlayerApiView,
    TabListApiView,
    TeamListApiView,
    TimelineListApiView,
    CsrfApiView,
    LogoutView,
    WebsocketApiView,
    NoteListApiView,
    Permission
)

urlpatterns = [
    path('club', ClubListApiView.as_view()),
    path('team', TeamListApiView.as_view()),
    re_path('team/(?P<id>\d+)', TeamListApiView.as_view(), name='team_by_id'),
    path('match', MatchListApiView.as_view()),
    path('matchInfo', MatchInfoListApiView.as_view()),
    re_path('matchInfo/(?P<id>\d+)', MatchInfoListApiView.as_view(), name='match_info_by_id'),
    path('permission', Permission.as_view()),
    path('action', ActionListApiView.as_view()),
    path('tab', TabListApiView.as_view()),
    path('tabType', TabListApiView.as_view()),
    path('websocket', WebsocketApiView.as_view()),
    re_path('websocket/(?P<id>\d+)', WebsocketApiView.as_view(), name='websocket'),
    path('event', EventListApiView.as_view()),
    path('note', NoteListApiView.as_view()),
    re_path('action/(?P<id>\d+)', ActionListApiView.as_view(), name='action'),
    re_path('match/(?P<id>\d+)', MatchListApiView.as_view(), name='match_by_id'),
    re_path('event/(?P<id>\d+)', EventListApiView.as_view(), name='event_by_match_id'),
    re_path('note/(?P<id>\d+)', NoteListApiView.as_view(), name='note_by_id'),
    path('timeline', TimelineListApiView.as_view()),
    path('csrf', CsrfApiView.as_view()),
    path('logout', LogoutView.as_view()),
    path('player', PlayerApiView.as_view()),
    re_path('player/(?P<id>\d+)', PlayerApiView.as_view(), name='player_by_id')
]