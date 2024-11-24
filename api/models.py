from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from enumfields import EnumField

from api.websocket import Websocket_status
from api.match_modes import Match_modes

# Create your models here

class Club(models.Model):
    name = models.CharField(max_length=30, unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    users = models.ManyToManyField(User)

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

class MatchInfo(models.Model):
    match = models.ForeignKey(Match, on_delete = models.CASCADE, null=True)
    yellow_card = models.PositiveIntegerField(null=True)
    yellow_card_opponent = models.PositiveIntegerField(null=True)
    red_card = models.PositiveIntegerField(null=True)
    red_card_opponent = models.PositiveIntegerField(null=True)
    goal = models.PositiveIntegerField(null=True)
    goal_opponent = models.PositiveIntegerField(null=True)
    substitution = models.PositiveIntegerField(null=True)
    substitution_opponent = models.PositiveIntegerField(null=True)
    corner = models.PositiveIntegerField(null=True)
    corner_opponent = models.PositiveIntegerField(null=True)

    def __str__(self):
        return "%s %s" % (self.match, self.id)

class Action(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)  # Hacemos opcional el match
    team = models.ForeignKey(Team, on_delete=models.CASCADE)    # Añadimos team opcional
    default = models.BooleanField()
    enabled = models.BooleanField()
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    events = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True, null=True)

    def clean(self):
        # Validamos que tenga o bien team o bien match, pero no ambos o ninguno
        if (self.team is None and self.match is None):
            raise ValidationError('Action debe estar asociada a un team O a un match, no a ambos o a ninguno')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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

class BaseEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, null=True, default='ACTIVE')
    delay_start = models.IntegerField()
    start = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delay_start = models.IntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s %s %s" % (self.match.id, self.action.id, self.id)
    
    def delete(self):
        self.status = 'DELETED'
        self.save()

class Event(BaseEvent):
    pass

class TemporalEvent(BaseEvent):
    end = models.IntegerField(null=True)
    delay_end = models.IntegerField(null=True)

class Player_posittion(Enum):
        GOALKEEPER = 'GOALKEEPER'
        DEFENDER = 'DEFENDER'
        MIDFIELDER = 'MIDFIELDER'
        FORWARD = 'FORWARD'

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    name = models.CharField(max_length=30)
    number = models.PositiveIntegerField()
    position = EnumField(Player_posittion)
    total_minutes = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s" % (self.team.id, self.name)

class Lineup(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)  # Asumiendo que tienes un modelo Match
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_starter = models.BooleanField(default=False)  # True si es titular, False si es suplente
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        # Asegura que un jugador no pueda estar dos veces en el mismo partido
        unique_together = ['match', 'player']

    def __str__(self):
        return f"{self.match} - {self.player.name} ({'Titular' if self.is_starter else 'Suplente'})"

