from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Club, Tab, Team, Match, Action, TabType, Note, Event, Websocket

admin.site.register(Club)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Action)
admin.site.register(Tab)
admin.site.register(TabType)
admin.site.register(Note)
admin.site.register(Event)
admin.site.register(Websocket)
