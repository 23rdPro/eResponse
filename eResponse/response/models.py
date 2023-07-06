"""
Emergency Model provides the identification, and the remedying activities at instantiation
There will be two major groups of Emergency: natural and synthetic, and must be associated
with at least one management level user.
"""

import logging
import eResponse

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class Emergency(eResponse.mixins.TimeMixin, eResponse.mixins.IDMixin):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='type')

    # all users regardless of groups however a manager must instantiate
    # this model hence, cannot be blank
    respondents = models.ManyToManyField(get_user_model(), related_name='experts')

    # each emergency may have multiple briefs
    briefs = models.ManyToManyField("Brief", related_name='briefs')

    class Severity(models.IntegerChoices):
        BAD: tuple = 1, "Bad"
        TERRIBLE: tuple = 2, "Terrible"
        CATACLYSMIC: tuple = 3, "Cataclysmic"

    severity = models.IntegerField(
        choices=Severity.choices,
        default=Severity.BAD,
        verbose_name="Severity"
    )

    class EmergencyQuerySet(models.QuerySet):
        def _check(self):
            try:
                assert self.filter().exists()
                assert 'experts' in self.filter(respondents__groups__name='experts')
                assert 'leads' in self.filter(respondents__groups__name='leads')
                assert 'managers' in self.filter(respondents__groups__name='managers')
            except Exception as error:
                logging.error(error)

        def experts(self):
            self._check()
            return self.filter(respondents__groups__name__contains='experts')

        def leads(self):
            self._check()
            return self.filter(respondents__groups__name__contains='leads')

        def managers(self):
            self._check()
            return self.filter(respondents__groups__name__contains='managers')

    objects = EmergencyQuerySet.as_manager()


class Brief(eResponse.mixins.TimeMixin, eResponse.mixins.IDMixin):
    title = models.CharField(_("Title Description"), max_length=255)
    text = models.TextField(_("Text"), max_length=500, blank=False, null=False)
    pictures = models.ManyToManyField("Picture", blank=True, related_name='pictures')
    videos = models.ManyToManyField("Video", blank=True, related_name='videos')
    objects = models.Manager()


class Picture(eResponse.mixins.TimeMixin, eResponse.mixins.IDMixin):
    picture = models.FileField(upload_to='jpegs/%Y/%m/%d/')
    objects = models.Manager()
    # attachments = models.FileField(upload_to=f'../media/{user.username}/') todo


class Video(eResponse.mixins.TimeMixin, eResponse.mixins.IDMixin):
    video = models.FileField(upload_to='tapes/%Y/%m/%d/')
    objects = models.Manager()
