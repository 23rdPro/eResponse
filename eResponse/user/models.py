import json
import os
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
)
from pathlib import Path
from typing import Any, Callable, Union
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from eResponse.mixins import TimeMixin, IDMixin
from eResponse.user.managers import UserManager

from eResponse.user.FastAPI.schemas import UserSchema


def avatars_path(instance: Any, filename: str) -> Union[str, Callable, Path]:
    """
    set up the default path for avatar uploads
    :param filename:
    :param instance:
    :return:
    """
    return os.path.join(*["avatars", instance.email, "%Y/%m/%d", filename])


class User(TimeMixin, IDMixin, AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(Group, related_name='groups')
    # not blank because every user belong to at least one group

    is_active = models.BooleanField(_('Active Status'), default=False)
    # active on this app, available to handle emergency
    is_available = models.BooleanField(_('Availability'), default=True)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_staff = models.BooleanField(_("Admin"), default=False)

    title = models.CharField(_('Title'), max_length=128)
    email = models.EmailField(_('Email Address'), unique=True, max_length=255)
    name = models.CharField(_('Full Name'), max_length=128, blank=True)
    mobile = PhoneNumberField()
    certifications = models.ManyToManyField("Certification",
                                            related_name='certificates')
    avatar = models.FileField(upload_to=avatars_path)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # none, to allow frontend auth flow

    class Meta:
        ordering = ['created_at', ]
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        if self.name and len(str(self.name).split()) < 2:
            raise ValidationError(_('Please provide your full name'))

    def display_name(self):
        return str(self.name).title()

    def save(self, *args, **kwargs):
        self.full_clean()
        instance = super(User, self).save(*args, **kwargs)
        return instance

    def get_absolute_url(self):
        return reverse('user:detail', kwargs={'id': self.id})

    @classmethod
    def from_api(cls, model: UserSchema):
        """
        returns a user instance from schema instance
        :param model:
        :return:
        """
        json_data = json.loads(model.json())
        return cls(
            id=json_data['id'],
            groups=json_data['groups'],
            is_active=json_data['is_active'],
            is_staff=json_data['is_staff'],
            is_available=json_data['is_available'],
            is_superuser=json_data['is_superuser'],
            title=json_data['title'],
            email=json_data['email'],
            name=json_data['name'],
            mobile=json_data['mobile'],
            certifications=json_data['certifications'],
            avatar=json_data['avatar'],
        )

    def update_from_api(self, model: UserSchema):
        """
        update user model with schema instance
        :return:
        """
        json_data: dict = json.loads(model.json())

        self.id = json_data.get('id', '')
        self.groups = json_data.get('groups', [])
        self.is_staff = json_data.get('is_staff', False)
        self.is_active = json_data.get('is_active', False)
        self.is_available = json_data.get('is_available', False)
        self.is_superuser = json_data.get('is_superuser', False)
        self.title = json_data.get('title', '')
        self.email = json_data.get('email', False)
        self.name = json_data.get('name', '')
        self.mobile = json_data.get('mobile', '')
        self.certifications = json_data.get('certifications', [])
        self.avatar = json_data.get('avatar', '')

    @classmethod
    def from_model(cls):
        pass

    @classmethod
    def from_qs(cls):
        pass


def cert_path(certificate: Any, filename: str) -> Union[str, Callable, Path]:
    return os.path.join(
        *["certificates",
          certificate.certificates.distinct().email,
          "%Y/%m/%d",
          filename
          ]
    )


class Certification(TimeMixin):
    title = models.CharField(_("Title"), max_length=128, )
    description = models.TextField(_('Describe achievement'), max_length=555)
    # department = models.Choices  # todo confirm from operations
    upload = models.FileField(upload_to=cert_path, blank=True, null=True)
