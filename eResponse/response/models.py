"""
Emergency Model provides the identification, and the remedying activities at instantiation
There will be two major groups of Emergency: natural and synthetic, and must be associated
with at least one management level user.
"""
import os.path
from typing import Optional
from asgiref.sync import sync_to_async
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

    # each emergency may have multiple briefs, cannot be blank **
    briefs = models.ManyToManyField("Brief", related_name='briefs', blank=True)

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
        def get_all_emergencies(self):
            return self.select_related(
                "emergency_type"
            ).prefetch_related("respondents", "briefs").all()

        async def aget_all_emergencies(self):
            return await sync_to_async(list)(self.get_all_emergencies())


        # async def afilter(self):
        #     return await sync_to_async(self.filter)()

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

    objects = models.Manager()
    filters = EmergencyQuerySet.as_manager()

    class Meta:
        verbose_name = "Emergency Response"
        verbose_name_plural = "Emergency Responses"


class Brief(mixins.TimeMixin, mixins.IDMixin):
    reporter = models.ForeignKey(UserModel, related_name="reporter", on_delete=models.CASCADE)
    title = models.CharField(_("Title Description"), max_length=255)
    text = models.TextField(_("Text"), max_length=500, blank=False, null=False)
    files = models.ManyToManyField("File", blank=True, related_name="files")
    objects = models.Manager()

    class Meta:
        verbose_name = "Brief"
        verbose_name_plural = "Briefs"


class File(mixins.TimeMixin, mixins.IDMixin):
    file = models.FileField(upload_to="files/%Y/%m/%d/")
    objects = models.Manager()

    def get_file_path_name(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.get_file_path_name()

    def save(self, *args, **kwargs):
        filename = self.generate_file()
        with open(filename, "rb") as f:
            self.file.save(filename, f, save=False)
        # delete file when done todo
        return super(File, self).save(*args, **kwargs)

    async def asave(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        return await sync_to_async(self.save)(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    @staticmethod
    def generate_file():
        import glob
        import os

        files = glob.glob("eResponse/media/responses/*")  # * means all, if specific format needed then *.csv
        latest = max(files, key=os.path.getctime)
        return latest

