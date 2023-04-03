from django.db import models
from django.utils import timezone


class ThreadEvent(models.Model):
    """
    Each event is a message. Messages in any ThreadEvent can either
    originate from a root (sender) or as a response to the received
    message to constitute a thread, -list of messages.
    role: for each thread, the first message is the root while others
    are responses
    """
    timestamp = models.DateTimeField(default=timezone.now)
    id = models.BigIntegerField(primary_key=True, editable=False, unique=True)
    role = models.ManyToManyField('Role')  # cannot be blank


ROLES = ((ROOT := "1", "ROOT"), (RESPONSE := "2", "RESPONSE"))


class Role(models.Model):
    role = models.CharField(max_length=1, choices=ROLES)
