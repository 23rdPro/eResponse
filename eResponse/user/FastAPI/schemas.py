from typing import List
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djantic import ModelSchema
from eResponse.user.models import Certification


class GroupSchema(ModelSchema):
    class Config:
        model = Group
        include = ['name', ]


class CertificationSchema(ModelSchema):
    class Config:
        model = Certification


class UserSchema(ModelSchema):
    groups: List[GroupSchema]
    certificates = List[CertificationSchema]

    class Config:
        model = get_user_model()

