import logging
import os

from abc import ABC
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand, ABC):
    def handle(self, *args, **options):
        dirname = os.path.join(settings.BASE_DIR / 'eResponse')
        try:
            for root, dirs, files in os.walk(dirname):
                if os.path.basename(root) == 'migrations':
                    for file in files:
                        if file != '__init__.py':
                            os.remove(os.path.join(root, file))
            self.stdout.write("Success")
        except CommandError as error:
            logging.error(error)
