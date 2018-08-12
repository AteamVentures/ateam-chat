# from django.contrib.auth.models import User
from django.db import models

from api.users.models import User
from django.utils import timezone


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.message

    def read(self):
        if not self.is_read:
            self.is_read = True
            self.date_read = timezone.now()
            self.save()
