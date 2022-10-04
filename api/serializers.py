# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Club, Team, Match, Action
from django.contrib.auth.models import User

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name']
class TeamSerializer(serializers.ModelSerializer):
    club = ClubSerializer()
    class Meta:
        model = Team
        fields = ['id', 'name', 'club']
class MatchSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = Match
        fields = ['id', 'name', 'timeline', 'team', 'media']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['name', 'color']
