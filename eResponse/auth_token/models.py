from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from eResponse import mixins


class Token(mixins.TimeMixin):
    token_type = models.CharField(default="bearer", editable=False,
                                  max_length=6)

    access_token = models.CharField(
        max_length=666, primary_key=True, editable=False, unique=True,
        db_index=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User"))

    objects = models.Manager()

    class Meta:
        verbose_name = "Token"
