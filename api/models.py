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

class Match(models.Model):
    name = models.CharField(max_length=30)
    timeline = models.URLField(max_length = 200)
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    media = models.URLField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    started_at = models.CharField(max_length=200, null=True)
    finished_at = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.team.name, self.id)

class Action(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    default = models.BooleanField()
    enabled = models.BooleanField()
    events = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)

    def __str__(self):
        return "%s %s" % (self.name, self.match)