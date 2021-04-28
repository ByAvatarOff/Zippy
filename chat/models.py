from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

