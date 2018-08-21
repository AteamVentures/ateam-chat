
import json
from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import User


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', db_constraint=False)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        if isinstance(self.handle, User):
            return {'handle': str(self.handle.display_name), 'message': self.message, 'timestamp': self.formatted_timestamp}
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
