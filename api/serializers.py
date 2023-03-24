# todo/todo_api/serializers.py
from rest_framework import serializers

from api.websocket import Websocket_status
from .models import Club, Tab, Team, Match, Action, Websocket, Event
from django.contrib.auth.models import User

class EnumChoiceField(serializers.Field):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        self.choices = [choice.value for choice in self.enum]
        super(EnumChoiceField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return obj.value

    def to_internal_value(self, data):
        try:
            return self.enum[data]
        except KeyError:
            self.fail('invalid_choice', input=data)

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
        fields = ['id', 'name', 'timeline', 'team', 'media', 'status', 'tab', 'created_at', 'started_at', 'finished_at']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id','name','key', 'color', 'match','enabled','events', 'default', 'status', 'updated_at', 'updated_by', 'created_at']
class TabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = ['id', 'name','icon','order']
class TabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = ['name']
class WebsocketSerializer(serializers.ModelSerializer):
    status = EnumChoiceField(Websocket_status, default=Websocket_status.OPENED)
    class Meta:
        model = Websocket
        fields = ['id','key','connection', 'updated_at', 'updated_by', 'created_at', 'match', 'status']
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','match','action', 'status', 'created_at', 'updated_at', 'updated_by', 'delay']
