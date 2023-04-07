# todo/todo_api/serializers.py
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.websocket import Websocket_status
from .models import Club, Tab, Team, Match, Action, Websocket, Event, TabType
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
        fields = ['id', 'username', 'email']
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
        model = TabType
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


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
