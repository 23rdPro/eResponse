from django.db import models
from django.utils import timezone


class ThreadEvent(models.Model):
    """
    Each event is a message. Messages in any ThreadEvent can either
    originate from a root (sender) or as a response to the received
    message to constitute a thread, -list of messages.
    role: for each thread, the first message is the root while others
    are responses
    This model is structured not on individual contents of messages,
    but on timestamps successively been recorded in the db format=minimal
    """
    timestamp = models.DateTimeField(default=timezone.now)
    # timestamp when new thread event is recorded the first time
    id = models.CharField(max_length=128, primary_key=True, editable=False, unique=True)
    roles = models.ManyToManyField('Role')  # cannot be blank
    objects = models.Manager()


class LastEventToken(models.Model):
    token = models.CharField(primary_key=True, unique=True, editable=False)
    objects = models.Manager()


class Role(models.Model):
    # role = models.CharField(max_length=1, choices=ROLES)
    id = models.CharField(max_length=128, primary_key=True, editable=False, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    # timestamps when multiple responses are being added to ThreadEvent.roles
    objects = models.Manager()
