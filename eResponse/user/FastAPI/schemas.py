import typing

from django.contrib.auth.models import Group
from djantic import ModelSchema
from eResponse.user import models


class GroupSchema(ModelSchema):
    name: str

    class Config:
        model = Group
        include = ['name', ]


class CertificationSchema(ModelSchema):
    qualification: str or None = None
    description: str or None = None
    # upload: str

    class Config:
        model = models.Certification
        include = ['qualification', 'description', ]


class UserRegistrationSchema(ModelSchema):
    class Config:
        model = models.User
        include = ["email", "password"]


class UpdateUserSchema(ModelSchema):
    class Config:
        model = models.User
        include = ["email", "name", "mobile", ]


class UpdateUserAvatar(ModelSchema):
    class Config:
        model = models.User
        include = ["avatar", ]


class UserSchema(ModelSchema):
    groups: typing.List[GroupSchema]
    certifications: typing.List[CertificationSchema]
    email: str or None = None

    class Config:
        model = models.User
        # fastapi model id field exclude from request todo
        include = ['email', "name", "groups", "is_available",
                   "mobile", "certifications",
                   ]
