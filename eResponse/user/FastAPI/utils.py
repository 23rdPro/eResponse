from __future__ import annotations

from datetime import timedelta, datetime
from asgiref.sync import sync_to_async
from typing import Union
from jose import jwt
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate
from djantic.main import ModelSchema
from eResponse import (
    ALGORITHM,
    API_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

from eResponse.user import models as user_models


@sync_to_async
def create_access_token_sync(
        data: dict,
        expires_delta: timedelta | None = None
):

    encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    encode.update({"exp": expire})
    encoded = jwt.encode(
        encode,
        API_SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded


@sync_to_async
def jwt_decode(token):

    return jwt.decode(
        token,
        API_SECRET_KEY,
        algorithms=[ALGORITHM]
    )


@sync_to_async
def to_schema(
        django_obj: Union[type(models), type(QuerySet)],
        schema: ModelSchema
):
    if hasattr(django_obj, "count"):
        if django_obj.count() > 1:
            return schema.from_django(django_obj, many=True)

        return schema.from_orm(django_obj.get())

    return schema.from_orm(django_obj)


@sync_to_async
def create_user_sync(**kwargs):
    user = user_models.User.objects.create_user(**kwargs)

    return user


@sync_to_async
def authenticate_user(email: str, password: str):
    user = authenticate(email=email, password=password)

    return user if user else None


@sync_to_async
def get_user_from_token(token: str):
    user = user_models.User.filters.get_users().filter(email=token)

    if user.exists():
        return user.get()
    return None


@sync_to_async
def get_all_users():
    return user_models.User.filters.get_users()


@sync_to_async
def filter_user_by_id(user_id: str):
    user = user_models.User.objects.filter(id=user_id)
    if user.exists():
        return user.get()
    return None


@sync_to_async
def get_user_from_payload(payload: dict):
    email = payload.get("sub")
    user = user_models.User.filters.get_users().filter(
        email=email
    ).distinct()

    user.update(is_active=True)
    return user.get()


@sync_to_async
def get_user_sync(**kwargs):
    user = user_models.User.objects.filter(**kwargs)
    if user.exists():
        return user.get()
    return


@sync_to_async
def create_group(**kwargs):
    return Group.objects.get_or_create(**kwargs)[0]


@sync_to_async
def create_certificate(**kwargs):
    certification = user_models.Certification(**kwargs)
    certification.save()
    return certification
