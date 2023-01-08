# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Club, Tab, Team, Match, Action, MatchAction
from django.contrib.auth.models import User

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name']
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'club']
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'name', 'timeline', 'team', 'media', 'created_at', 'started_at', 'finished_at']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id','name','key', 'color', 'match', 'created_at', 'events', 'default', 'enabled', 'updated_at']
class TabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = ['name','icon','order']
class MatchActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchAction
        fields = ['match','action']
