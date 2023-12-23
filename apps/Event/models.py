from django.db import models
from django.contrib.auth.models import User

from ...api.models import Match, Action

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