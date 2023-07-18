import typing

from django.contrib.auth.models import Group
from djantic import ModelSchema
from eResponse.user import models


class GroupSchema(ModelSchema):
    class Config:
        model = Group
        include = ['name', ]


class CertificationSchema(ModelSchema):
    class Config:
        model = models.Certification
        include = ['title', 'description', 'upload']


class UserSchema(ModelSchema):
    groups: typing.List[GroupSchema]
    certifications: typing.List[CertificationSchema]
    # avatar: typing.Optional[str] = None todo

    class Config:
        model = models.User
        include = ['email', "password", "name", "is_active",
                   "is_superuser", "is_staff", "groups",
                   "is_available", "title", "mobile",
                   "certifications", ]

