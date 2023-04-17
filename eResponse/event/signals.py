from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from eResponse.event.models import ThreadEvent


@receiver(post_save, sender=ThreadEvent)
def role_response_time_signal(sender, instance, **kwargs):
    prev = None
    # async events will trigger this signal,
    # it's important to note db integrity
    with transaction.atomic():
        for message in instance.roles.all():
            if prev is None:
                prev = message.timestamp

            if not message.response_time:
                mean = ((message.timestamp-instance.timestamp) +
                        (message.timestamp-prev)) / 2
                message.response_time = mean.total_seconds()

            prev = message.timestamp
