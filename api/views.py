from django.shortcuts import render
from django.middleware.csrf import get_token

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Team, Match, Action, Club
from .serializers import ClubSerializer, TeamSerializer, MatchSerializer, ActionSerializer
from .timeline import Timeline
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import get_match_by_id
import json, datetime
from django.core.exceptions import PermissionDenied

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
            print('hey')
            token = RefreshToken(refresh_token)
            token.blacklist()
            print('hey')
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

    def get(self, request,id, *args, **kwargs):
        team_ids_req = request.query_params.getlist('teams')
        if team_ids_req:
            team_ids = strToArr(team_ids_req[0])
            match = Match.objects.filter(team__id__in=team_ids)
            serializer = MatchSerializer(match, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            match = get_match_by_id(id,request.user)
            if match is not False:
                serializer = MatchSerializer(match)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        new_id = (Match.objects.last()).id
        data = {
            'id': new_id + 1,
            'name': request.data.get('name'), 
            'timeline': request.data.get('timeline'), 
            'team': request.data.get('team'), # team id
            'media': request.data.get('media'), 
        }
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            class actions: 
                def __init__(self, name, color, match, created_at, enabled, default, events):
                    self.name = name 
                    self.color = color
                    self.match = match
                    self.created_at = created_at
                    self.enabled = enabled
                    self.default = default
                    self.events = events
            default_buttons = []
            default_buttons.append( actions('goal', "#5557df", new_id +1, datetime.datetime.now(), True, True, []))
            default_buttons.append( actions('kick_off', "#a7df68", new_id +1, datetime.datetime.now(), True, True, []))
            default_buttons.append( actions('first_half', "#cbcbcb", new_id +1, datetime.datetime.now(), True, True, []))
            default_buttons.append( actions('second_half', "#787878", new_id +1, datetime.datetime.now(), True, True, []))
            default_buttons.append( actions('end', "#f1ae57", new_id +1, datetime.datetime.now(), True, True, []))
            
            for button in default_buttons:
                data = {
                    'name': button.name,
                    'color': button.color,
                    'created_at': button.created_at,
                    'match': button.match,
                    'enabled': button.enabled,
                    'default': button.default,
                    'events': []
                }
                action_serializer = ActionSerializer(data=data)
                if action_serializer.is_valid():
                    action_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        match_ids_req = request.query_params.getlist('matches')
        default_actions_req = request.query_params.get('default')
        match_ids = strToArr(match_ids_req[0])
        if default_actions_req:
            default_action_param = json.loads(default_actions_req.lower())
            actions = Action.objects.filter(match__id__in=match_ids, default=default_action_param)
        else:
            actions = Action.objects.filter(match__id__in=match_ids)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id, *args, **kwargs):
        action_id_req = id
        action_res = Action.objects.get(id=action_id_req)
        now = datetime.datetime.now()
        action_res.events = request.data.get('events')
        action_res.save()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        action_name = request.data.get('name')
        data = {
            'name': action_name,
            'color': request.data.get('color'),
            'match': request.data.get('match'),
            'enabled': request.data.get('enabled'),
            'default': request.data.get('default'),
            'events': []
        }
        serializer = ActionSerializer(data=data)
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

class TimelineListApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        match_ids_req = request.query_params.getlist('matches')
        match_ids = strToArr(match_ids_req[0])
        actions = Action.objects.filter(match__id__in=match_ids)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)