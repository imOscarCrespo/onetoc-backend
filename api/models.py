from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here

class Club(models.Model):
    name = models.CharField(max_length=30, unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=30)
    club = models.ForeignKey(Club, on_delete = models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return "%s %s %s" % (self.name, self.club, self.users)

class TabType(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)

class Tab(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    order = models.PositiveBigIntegerField()
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(TabType, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.order)


class Match(models.Model):
    name = models.CharField(max_length=30)
    timeline = models.URLField(max_length = 200, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    media = models.URLField(max_length = 200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    started_at = models.CharField(max_length=200, null=True)
    finished_at = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=30, null=True)
    tab = models.ForeignKey(Tab, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.team.name, self.id)

class Action(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30)
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    default = models.BooleanField()
    enabled = models.BooleanField()
    status = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    events = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.match, self.id)
        
class Event(models.Model):
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    action = models.ForeignKey(Action, on_delete = models.CASCADE)
    status = models.CharField(max_length=30, null=True)
    delay = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return "%s %s %s" % (self.match.id, self.action.id, self.id)