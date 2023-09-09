from django.middleware.csrf import get_token
from api.action.action import create_action

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from api.websocket import Websocket_status
from .models import Tab, TabType, Team, Match, Action, Club, Websocket, Event, User
from .request_utils.paginator import paginate
from .serializers import ClubSerializer, TabTypeSerializer, TabSerializer, TeamSerializer, MatchSerializer, \
    ActionSerializer, WebsocketSerializer, EventSerializer
from .models import Tab, TabType, Team, Match, Action, Club, Note
from .serializers import ClubSerializer, TabTypeSerializer, TabSerializer, TeamSerializer, MatchSerializer, ActionSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_match_by_id
import json
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.utils import timezone
from api.match_modes import Match_modes

def stringToInt(str):
    return int(str)

def strToArr(str):
    arr = str.split(',')
    new = map(stringToInt, arr)
    return list(new)

class CsrfApiView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        List all the club items for given requested user
        '''
        return Response({'csrfToken': get_token(request)}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ClubListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''
        List all the club items for given requested user
        '''
        teams_query = Team.objects.filter(users__username=request.user)
        def return_club(team):
            return team.club
        clubs = map(return_club, teams_query)
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }
        serializer = ClubSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        teams = Team.objects.filter(users__username=request.user)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        club_name = request.data.get('club_name')
        club = Club.objects.get(name=club_name)
        data = {
            'name': request.data.get('name'),
            'club': club
        }
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id=False, *args, **kwargs):
        if id:
            match = get_match_by_id(id,request.user)
            if match is not False:
                serializer = MatchSerializer(match)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied()
        else:
            query_data={}
            team_ids_req = request.query_params.getlist('teams')
            tab_id = request.query_params.get('tab')
            skip = request.query_params.get('skip')
            text_search = request.query_params.get('textSearch')
            if team_ids_req:
                team_ids = strToArr(team_ids_req[0])
                query_data['team__id__in'] = team_ids
            if tab_id is not None:
                query_data['tab__id'] = tab_id
            if text_search is not None:
                query_data['name__icontains'] = text_search
            match = Match.objects.filter(**query_data).order_by('-created_at').exclude(status='DELETED')
            page_records = paginate(match, skip)
            serializer = MatchSerializer(page_records, many=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response['x-total'] = match.count()
            return response

    def post(self, request, *args, **kwargs):
        try:
            new_id = (Match.objects.last()).id
        except:
            new_id = 0
        data = {
            'id': new_id + 1,
            'name': request.data.get('name'),
            'timeline': None,
            'status': 'PUBLISHED',
            'team': request.data.get('team'), # team id
            'media': None,
            'tab': request.data.get('tab'), # tab id
        }
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            class actions:
                def __init__(self, name, key, color, match, status, enabled, default, events):
                    self.key = key
                    self.name = name
                    self.color = color
                    self.match = match
                    self.enabled = enabled
                    self.default = default
                    self.events = events
                    self.status = "PUBLISHED"
            default_buttons = [actions('Inicio', 'kick_off', "#a7df68", new_id + 1, 'PUBLISHED', True, True, None),
                               actions('1 Parte', 'first_half', "#cbcbcb", new_id + 1, 'PUBLISHED', True, True, None),
                               actions('2 Parte', 'second_half', "#787878", new_id + 1, 'PUBLISHED', True, True, None),
                               actions('Final', 'end', "#f1ae57", new_id + 1, 'PUBLISHED', True, True, None)]

            for button in default_buttons:
                data = {
                    'key': button.key,
                    'name': button.name,
                    'color': button.color,
                    'match': button.match,
                    'status': button.status,
                    'enabled': button.enabled,
                    'default': button.default,
                    'events': button.events,
                    'updated_by': request.user.pk
                }
                action_serializer = ActionSerializer(data=data)
                if action_serializer.is_valid():
                    action_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        match = Match.objects.get(id=id)
        media_url = request.data.get('media')
        started_at = request.data.get('started')
        finished_at = request.data.get('finished')
        mode = request.data.get('mode')
        data = {}
        if media_url is not None:
            match.media = media_url
            data['media'] = media_url
        if started_at:
            match.started_at = timezone.now()
            data['started_at'] = timezone.now()
        if finished_at:
            match.finished_at = timezone.now()
            data['finished_at'] = timezone.now()
            match.mode = Match_modes.HISTORY
        if mode:
            match.mode = mode
            data['mode'] = mode
        match.save()
        return Response(data,status=status.HTTP_200_OK)

class ActionListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        match_ids_req = request.query_params.getlist('matches')
        default_actions_req = request.query_params.get('default')
        match_ids = strToArr(match_ids_req[0])
        if default_actions_req:
            default_action_param = json.loads(default_actions_req.lower())
            actions = Action.objects.filter(match__id__in=match_ids, default=default_action_param).order_by('updated_at')
        else:
            actions = Action.objects.filter(match__id__in=match_ids).order_by('updated_at')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id, *args, **kwargs):
        action_id_req = id
        action_res = Action.objects.get(id=action_id_req)
        enabled_req = request.data.get('enabled')
        # has_to_disable = False
        # actions_to_disable_once = ['kick_off','first_half','second_half','end']
        action_res.events = request.data.get('events')
        # if action_res.name in actions_to_disable_once:
        #     has_to_disable = True
        if enabled_req is not None:
            action_res.enabled = enabled_req
        # if action_res.name == 'kick_off':
        #     action_match = Match.objects.get(id=action_res.match.id)
        #     started_at = action_res.events[0]
        #     action_match.started_at = started_at
        #     action_match.save()
        # elif action_res.name == 'end':
        #     finished_at = action_res.events[0]
        #     action_match = Match.objects.get(id=action_res.match.id)
        #     action_match.finished_at = finished_at
        #     action_match.save()
        # action_res.events = request.data.get('events')
        # if has_to_disable == True:
        #     action_res.enabled = False
        action_res.save()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        action_name = request.data.get('name')
        serializer = create_action(action_name, request.data.get('color'),request.data.get('match'), request.data.get('default'), request.user.pk )
        if serializer.is_valid():
            serializer.save()
            # if action_name == 'full_time':
            #     actions = Action.objects.filter(match__id=request.data.get('match')).values()
            #     timeline = Timeline(request.data.get('match'), request.user, actions)
            #     timeline = timeline.generate()
            #     match = Match.objects.get(id=request.data.get('match'))
            #     match.timeline = timeline
            #     match.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TabListApiView(APIView):
    def get(self, request, *args, **kwargs):
        team_id = request.query_params.get('team')
        tabs = Tab.objects.filter(team=team_id).order_by('order')
        serializer = TabSerializer(tabs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'icon': request.data.get('icon'),
            'order': request.data.get('order'),
            'type': request.data.get('type'),
        }
        serializer = TabSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TabTypeListApiView(APIView):
    def get(self, request, *args, **kwargs):
        tab_types = TabType.objects.all().order_by('created_at')
        serializer = TabTypeSerializer(tab_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }
        serializer = TabTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventListApiView(APIView):
    def get(self, request, *args, **kwargs):
        match_id = request.query_params.get('match')
        events = Event.objects.filter(match_id=match_id).exclude(status='DELETED')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'match': request.data.get('match'),
            'action': request.data.get('action'),
            'created_at': request.data.get('createdAt') - timedelta(seconds=5) if request.data.get('createdAt') else datetime.now() - timedelta(seconds=5),
            'status': "PUBLISHED",
            'delay': request.data.get('delay') if request.data.get('delay') else 0,
            'updated_by': request.user.pk,
            'disabled': False
        }
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None, *args, **kwargs):
        event_id = id
        if event_id:
            event_to_update = Event.objects.get(id=event_id)
            action_id = request.data.get('action_id')
            delay = request.data.get('delay')
            status_code = request.data.get('status')
            if action_id:
                event_to_update.action = action_id
            if delay:
                event_to_update.delay = delay
            if status_code:
                event_to_update.status = status_code
            event_to_update.updated_by = User.objects.get(id=request.user.pk)
            event_to_update.save()
        else:
            props_to_update = request.data.get('update')
            ids_to_update = request.data.get('ids')
            events_to_update = Event.objects.filter(id__in=ids_to_update)
            for event in events_to_update:
                for key, value in props_to_update.items():
                    setattr(event, key, value)
                event.save()
        return Response(status=status.HTTP_200_OK)

class WebsocketApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id=False, *args, **kwargs):
        if id:
            websocket = Websocket.objects.get(id=id)
            print(websocket)
            if websocket is not False:
                serializer = WebsocketSerializer(websocket)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied()
        else:
            query_data={}
            websocket_key_req = request.query_params.get('key')
            websocket_match_req = request.query_params.get('match')
            if websocket_key_req is not None:
                query_data['key'] = websocket_key_req
            if websocket_match_req is not None:
                query_data['match__id'] = websocket_match_req
            websocket = Websocket.objects.filter(**query_data).order_by('created_at')
            serializer = WebsocketSerializer(websocket, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'connection': request.data.get('connection'),
            'key': request.data.get('key'),
            'updated_by': request.user.pk
        }
        serializer = WebsocketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        websocket = Websocket.objects.get(id=id)
        websocket_status = request.data.get('status')
        websocket_match = request.data.get('match')
        data = {}
        if websocket_status and websocket_status not in [member.value for member in Websocket_status]:
            return Response('Websocket status value is incorrect', status=status.HTTP_400_BAD_REQUEST)
        if websocket_status in [member.value for member in Websocket_status]:
            websocket.status = websocket_status
            data['status'] = websocket_status
        if websocket_match is not None:
            match = Match.objects.get(id=id)
            websocket.match = match
            data['match'] = websocket_match
        websocket.save()
        return Response(data,status=status.HTTP_200_OK)


class NoteListApiView(APIView):
    def get(self, request, id=False, *args, **kwargs):
        team_id_req = request.query_params.get('team')
        tab_id = request.query_params.get('tab')
        if id:
            note = Note.objects.get(id=id)
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            query_data = {}
            query_data['status'] = 'PUBLISHED'
            if tab_id is not None:
                query_data['tab__id'] = tab_id
            if team_id_req is not None:
                query_data['team__id'] = team_id_req
            notes = Note.objects.filter(**query_data).order_by('created_at')
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'team': request.data.get('team'),
            'tab': request.data.get('tab'),
            'description': request.data.get('description'),
            'status': 'PUBLISHED',
            'updated_by': request.user.pk
        }
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        note_to_update = Note.objects.get(id=id)
        if request.data.get('name'):
            note_to_update.name = request.data.get('name')
        if request.data.get('description'):
            note_to_update.description = request.data.get('description')
        if request.data.get('status'):
            note_to_update.status = request.data.get('status')
        note_to_update.save()
        return Response(status=status.HTTP_200_OK)

class TimelineListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        match_ids_req = request.query_params.getlist('matches')
        match_ids = strToArr(match_ids_req[0])
        actions = Action.objects.filter(match__id__in=match_ids)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)