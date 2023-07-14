from django.contrib.auth.models import Group
from djantic import ModelSchema
from rest_framework.authtoken.models import Token
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

    class Config:
        model = models.User
        include = ['email', "password", ]


class TokenSchema(ModelSchema):
    access_token: str
    token_type: str


class TokenData(ModelSchema):
    email: str
