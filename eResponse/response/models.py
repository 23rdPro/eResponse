import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class EmergencyEvent(models.Model):
    estatus = (
        (NOT_HANDLED    := '1', 'NOT_HANDLED'),
        (BEING_HANDLED  := '2', 'BEING_HANDLED'),
        (HANDLED        := '3', 'HANDLED'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    managers = models.ManyToManyField(get_user_model())
    actors = models.ManyToManyField(get_user_model())
    status = models.CharField(max_length=1, choices=estatus)
    reports = models.ManyToManyField('Report')
    timestamp = models.DateTimeField(default=timezone.now)


class Report(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.OneToOneField(EmergencyEvent, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    attachments = models.FileField(upload_to=f'../media/{user.username}/')
    timestamp = models.DateTimeField(default=timezone.now)

    def verify_attachments(self):
        if self.attachments > 2048:
            raise
        return self.attachments < 2048  # todo
