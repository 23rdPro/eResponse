"""
Emergency Model provides the identification, and the remedying activities at instantiation
There will be two major groups of Emergency: natural and synthetic, and must be associated
with at least one management level user.
"""

from typing import Optional
from eResponse import mixins

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

UserModel = settings.AUTH_USER_MODEL


class Emergency(mixins.TimeMixin, mixins.IDMixin):
    emergency_type = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='type')
    # synthetic and natural emergencies

    # all users regardless of group however a manager must instantiate
    # this model hence, cannot be blank
    respondents = models.ManyToManyField(UserModel, related_name='experts')

    # each emergency may have multiple briefs, cannot be blank
    briefs = models.ManyToManyField("Brief", related_name='briefs')

    class EmergencySeverity(models.IntegerChoices):
        BAD: tuple = 1, "Bad"
        TERRIBLE: tuple = 2, "Terrible"
        CATACLYSMIC: tuple = 3, "Cataclysmic"

    severity = models.IntegerField(
        choices=EmergencySeverity.choices,
        default=EmergencySeverity.BAD,
        verbose_name="Severity"
    )

    class EmergencyQuerySet(models.QuerySet):
        def get_all_experts(self):
            return self.filter(respondents__groups__name='experts').all()

        def get_all_managers(self):
            return self.filter(respondents__groups__name="managers").all()

        def get_all_leads(self):
            return self.filter(respondents__groups__name="leads").all()

        def get_all_briefs(self):
            return self.prefetch_related("briefs").all()

        def get_briefs_by_group(self, group: str):
            return self.get_all_briefs().filter(reporter__groups__name=group).all()

        def get_briefs_by_user(self, user: Optional[str]):
            """id, email or username"""
            return self.get_all_briefs().filter(
                Q(reporter__id=user) | Q(reporter__email=user)
            ).all()

    objects = EmergencyQuerySet.as_manager()

    class Meta:
        verbose_name = "Emergency Response"
        verbose_name_plural = "Emergency Responses"


class Brief(mixins.TimeMixin, mixins.IDMixin):
    reporter = models.ForeignKey(UserModel, related_name="reporter", on_delete=models.CASCADE)
    title = models.CharField(_("Title Description"), max_length=255)
    text = models.TextField(_("Text"), max_length=500, blank=False, null=False)
    pictures = models.ManyToManyField("Picture", blank=True, related_name='pictures')
    videos = models.ManyToManyField("Video", blank=True, related_name='videos')
    objects = models.Manager()

    class Meta:
        verbose_name = "Brief"
        verbose_name_plural = "Briefs"


class Picture(mixins.TimeMixin, mixins.IDMixin):
    picture = models.FileField(upload_to='photos/%Y/%m/%d/')
    objects = models.Manager()


class Video(mixins.TimeMixin, mixins.IDMixin):
    video = models.FileField(upload_to='videos/%Y/%m/%d/')
    objects = models.Manager()
