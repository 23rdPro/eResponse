from typing import List
from django.conf import settings
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


UserModel = settings.AUTH_USER_MODEL


class UserSchema(ModelSchema):
    groups: List[GroupSchema]
    certificates = List[CertificationSchema]

    class Config:
        model = UserModel

