"""
Warning!!!
This command will unload the connected db instance
todo: shell prompt for user email and filter for superuser status
"""

import logging

from abc import ABC
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand, ABC):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
