# todo/todo_api/serializers.py
from rest_framework import serializers

from api.websocket import Websocket_status
from api.match_modes import Match_modes
from .models import Club, Player, Player_posittion, Tab, Team, Match, Action, Note, TemporalEvent, Websocket, Event, MatchInfo, Lineup
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
        fields = ['id','name']
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'club']
class MatchSerializer(serializers.ModelSerializer):
    mode = EnumChoiceField(Match_modes, default=Match_modes.LIVE)
    class Meta:
        model = Match
        fields = ['id', 'name', 'timeline', 'team', 'media', 'status', 'tab', 'created_at', 'started_at', 'finished_at', 'mode']
class MatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchInfo
        fields = ['id', 'yellow_card', 'yellow_card_opponent', 'red_card', 'red_card_opponent', 'goal', 'goal_opponent', 'substitution', 'substitution_opponent','corner', 'corner_opponent', 'match']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id','name','key', 'color', 'match', 'team', 'enabled','events', 'default', 'status', 'updated_at', 'updated_by', 'created_at']
class TabSerializer(serializers.ModelSerializer):
    tabType = serializers.CharField(source='type.name', read_only=True)
    class Meta:
        model = Tab
        fields = ['id', 'name','icon','order','type', 'tabType']
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
        fields = ['id','match','action', 'status', 'created_at', 'updated_at', 'updated_by', 'start', 'delay_start']

class TemporalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalEvent
        fields = ['id','match','action', 'status', 'created_at', 'updated_at', 'updated_by', 'start', 'end', 'delay_start', 'delay_end']
class NoteSerializer(serializers.ModelSerializer):
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True)
    class Meta:
        model = Note
        fields = ['id','name','team', 'description', 'status', 'updated_at', 'created_at', 'updated_by', 'updated_by_name', 'tab']
class PlayerSerializer(serializers.ModelSerializer):
    position = EnumChoiceField(Player_posittion, default=Match_modes.LIVE)
    class Meta:
        model = Player
        fields = ['id','name','team', 'number', 'total_minutes', 'position', 'updated_at', 'created_at', 'updated_by']
class LineupSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = Lineup
        fields = ['id', 'match', 'player', 'is_starter', 'created_at', 'updated_at', 'updated_by']
        read_only_fields = ['created_at', 'updated_at']

class LineupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lineup
        fields = ['match', 'player', 'is_starter', 'updated_by']
