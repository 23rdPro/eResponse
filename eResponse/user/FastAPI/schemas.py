import re
import typing

from django.contrib.auth.models import Group
from pydantic import BaseModel, validator, ValidationError
from djantic import ModelSchema
from phonenumber_field.modelfields import PhoneNumberField
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


class MobilePhoneFieldSchema(BaseModel):
    phone_number: typing.Any

    @classmethod
    @validator("phone_number", pre=True)
    def phone_number_validation(cls, v):
        v = str(v)
        # regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        # if v and not re.search(regex, v, re.I):
        #     raise ValueError("Phone number invalid")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True


def from_PhoneNumberField(raw: PhoneNumberField) -> str:
    return str(raw)


class UpdateUserSchema(ModelSchema):
    is_available: bool or None = None
    is_active: bool or None = None
    # mobile: MobilePhoneFieldSchema or None = None
    mobile: str

    _mobile = validator("mobile", pre=True, allow_reuse=True)(from_PhoneNumberField)

    class Config:
        model = models.User
        include = ["name", "mobile", "is_available", "is_active"]


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
