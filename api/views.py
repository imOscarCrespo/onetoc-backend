from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Team, Match, Action, Club
from .serializers import ClubSerializer, TeamSerializer, MatchSerializer, ActionSerializer
from .timeline import Timeline

def stringToInt(str):
    return int(str)

def strToArr(str):
    arr = str.split(',')
    new = map(stringToInt, arr)
    return list(new)
    


class ClubListApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

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

    permission_classes = [permissions.IsAuthenticated]

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

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        team_ids_req = request.query_params.getlist('teams')
        team_ids = strToArr(team_ids_req[0])
        match = Match.objects.filter(team__id__in=team_ids)
        serializer = MatchSerializer(match, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'), 
            'timeline': request.data.get('timeline'), 
            'team': request.data.get('team'), # team id
            'media': request.data.get('media'), 
        }
        serializer = MatchSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionListApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        match_ids_req = request.query_params.getlist('matches')
        match_ids = strToArr(match_ids_req[0])
        actions = Action.objects.filter(match__id__in=match_ids)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        action_name = request.data.get('name')
        data = {
            'name': action_name,
            'color': request.data.get('color'),
            'match': request.data.get('match') 
        }
        serializer = ActionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if action_name == 'full_time':
                actions = Action.objects.filter(match__id=request.data.get('match')).values()
                timeline = Timeline(request.data.get('match'), request.user, actions)
                timeline = timeline.generate()
                match = Match.objects.get(id=request.data.get('match'))
                match.timeline = timeline
                match.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)