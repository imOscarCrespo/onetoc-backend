from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField
from enumfields import EnumField

from api.websocket import Websocket_status
from api.match_modes import Match_modes
from api.enums.user_types import User_types
from api.enums.gender import Gender

# Create your models here

class Club(models.Model):
    name = models.CharField(max_length=30, unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=30)
    club = models.ForeignKey(Club, on_delete = models.CASCADE)
    users = models.ManyToManyField(User)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')

    def __str__(self):
        return "%s %s %s" % (self.name, self.club, self.users)
    
    def delete(self, user):
        self.status = 'DELETED'
        self.save()

class TabType(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')

    def __str__(self):
        return "%s" % (self.name)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class Tab(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    order = models.PositiveBigIntegerField()
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(TabType, on_delete = models.CASCADE, null=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.order)
    
    def delete(self):
        self.status = 'DELETED'
        self.save() 


class Match(models.Model):
    name = models.CharField(max_length=30)
    timeline = models.URLField(max_length = 200, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    media = models.URLField(max_length = 200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    started_at = models.CharField(max_length=200, null=True)
    finished_at = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    tab = models.ForeignKey(Tab, on_delete = models.CASCADE, null=True)
    mode = EnumField(Match_modes, default=Match_modes.LIVE)

    def __str__(self):
        return "%s %s %s" % (self.name, self.team.name, self.id)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class Action(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30)
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    default = models.BooleanField()
    enabled = models.BooleanField()
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    events = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.match, self.id)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class Websocket(models.Model):
    match = models.ForeignKey(Match, on_delete = models.CASCADE, null=True)
    key = models.CharField(max_length=30, unique=True)
    connection = models.CharField(max_length=30)
    status = EnumField(Websocket_status, default=Websocket_status.OPENED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.connection, self.match, self.status)

class Note(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    tab = models.ForeignKey(Tab, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.id, self.team.id)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class Event(models.Model):
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    action = models.ForeignKey(Action, on_delete = models.CASCADE)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    delay = models.FloatField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s %s" % (self.match.id, self.action.id, self.id)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class BaseOnetocUser(models.Model):
    first_name  = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, null=True)
    phone = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    gender = EnumField(Gender)
    age = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    class Meta:
        abstract = True

class Coach(BaseOnetocUser):
    type = EnumField(User_types, default=User_types.COACH)
    pass

class Analyst(BaseOnetocUser):
    type = EnumField(User_types, default=User_types.ANALYST)
    pass

class Player(BaseOnetocUser):
    type = EnumField(User_types, default=User_types.PLAYER)
    shoe_size = models.CharField(max_length=30)

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    type = type = EnumField(User_types)