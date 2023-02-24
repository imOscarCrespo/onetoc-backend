# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Club, Tab, Team, Match, Action, Note
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
        fields = ['id', 'name', 'timeline', 'team', 'media', 'status', 'created_at', 'started_at', 'finished_at']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id','name','key', 'color', 'match','enabled','events', 'default', 'status', 'updated_at', 'updated_by', 'created_at']
class TabSerializer(serializers.ModelSerializer):
    tabType = serializers.CharField(source='type.name', read_only=True)
    class Meta:
        model = Tab
        fields = ['id', 'name','icon','order','type', 'tabType']
class TabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = ['name']
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','name','team', 'description', 'status', 'updated_at', 'updated_by', 'created_at']
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['match','action', 'status', 'disabled', 'created_at', 'updated_at', 'updated_by']
