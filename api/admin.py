from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Club, Team, Match, Action

admin.site.register(Club)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Action)