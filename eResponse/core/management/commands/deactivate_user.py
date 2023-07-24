import logging

from abc import ABC
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from eResponse.user.models import User


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        users = User.objects.filter(is_active=False)
        try:
            for user in users:
                if (timezone.now() - user.created_at).days() > 6:
                    user.delete()
        except CommandError as error:
            logging.error(error)
