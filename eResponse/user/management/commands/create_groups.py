"""
Create permission groups
Create permissions to models for a set of groups
"""

import logging
from abc import ABC
from collections import ChainMap

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


READ_PERMISSIONS = ['can_view_emergency', 'can_respond_to_emergency', ]
SEMI_WRITE_PERMISSIONS = ['can_add_emergency', 'can_change_emergency', ]
FULL_WRITE_PERMISSIONS = ['can_delete_emergency', ]

READ = {code: ' '.join(code.split('_')).capitalize() for code in READ_PERMISSIONS}
SEMI_WRITE = {code: ' '.join(code.split('_')).capitalize() for code in SEMI_WRITE_PERMISSIONS}
FULL_WRITE = {code: ' '.join(code.split('_')).capitalize() for code in FULL_WRITE_PERMISSIONS}

GROUPS = [('lead', 'semi'), ('manager', 'full'), ('expert', 'read')]


class Command(BaseCommand, ABC):
    help = 'Creates default permission and groups for users'

    def handle(self, *args, **options):
        """
        a team lead has semi permission, an expert has read permission only
        a manager has full permission
        """
        try:
            content = ContentType.objects.get_for_model(get_user_model())

            for group, perm in GROUPS:
                gp, created = Group.objects.get_or_create(name=group)

                if perm == 'semi':  # todo bulk_create does not support m2m
                    permissions = Permission.objects.bulk_create([
                        Permission(codename=k, name=v, content_type=content)
                        for k, v in ChainMap(READ, SEMI_WRITE).items()
                    ])
                elif perm == 'full':
                    permissions = Permission.objects.bulk_create([
                        Permission(codename=k, name=v, content_type=content)
                        for k, v in ChainMap(READ, SEMI_WRITE, FULL_WRITE).items()
                    ])
                else:
                    permissions = Permission.objects.bulk_create([
                        Permission()
                        for k, v in READ.items()
                    ])

                gp.permissions.add(permissions)
            print("Success!!!")

        except Exception as error:
            logging.warning(error)
