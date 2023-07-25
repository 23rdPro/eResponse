from __future__ import annotations

from datetime import timedelta, datetime
from asgiref.sync import sync_to_async
from typing import Any
from jose import jwt, JWTError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate
from djantic.main import ModelSchema
from eResponse import oauth2_scheme, pwd_context, ALGORITHM, API_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from eResponse.user import models as user_models
from eResponse.auth_token import models as auth_token_models


@sync_to_async
def create_access_token_sync(data: dict, expires_delta: timedelta | None = None):
    encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    encode.update({"exp": expire})
    encoded = jwt.encode(encode, API_SECRET_KEY, algorithm=ALGORITHM)
    return encoded


@sync_to_async
def jwt_decode(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[ALGORITHM])


@sync_to_async
def to_schema(django_obj: Any[models, QuerySet], schema: ModelSchema):
    if hasattr(django_obj, "count"):  # queryset.count
        return schema.from_django(django_obj, many=True)
    return schema.from_orm(django_obj)


@sync_to_async
def from_schema(model: models, schema: ModelSchema) -> None:
    """
    create model instance from response schema
    :param model:
    :param schema:
    :return:
    """
    instance = model.from_api(schema)
    try:
        instance.save()
    except Exception as Error:
        raise Error
    return


@sync_to_async
def create_user_sync(**kwargs):
    user = user_models.User.objects.create_user(**kwargs)
    return user


@sync_to_async
def get_object_token(token: str):
    print(token)


@sync_to_async
def activate_user_sync(user: user_models.User, token):
    assert auth_token_models.Token.objects.filter(user__id=user.id).exists()
    assert auth_token_models.Token.filters.filter_by_fields()
    """
    user regitsers
    comes back procedure
    """
    assert user_models.User.objects.filter(id=user.id).exists()
    user.is_active = True
    user.save()
    return user.is_active is True


@sync_to_async
def update_user_sync(user: models, schema):
    user.update(**schema.dict())
    user.save()
    return user


@sync_to_async
def authenticate_user(email: str, password: str):
    user = authenticate(email=email, password=password)
    return user if user else None


@sync_to_async
def convert_to_model(**kwargs):
    pass


@sync_to_async
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@sync_to_async
def get_user_from_token(token: str):
    user = user_models.User.users.get_users().filter(email=token)
    if user.exists():
        return user.get()
    return None


@sync_to_async
def get_all_users():
    return user_models.User.users.get_users()


@sync_to_async
def filter_user_by_id(user_id: str):
    user = user_models.User.objects.filter(id=user_id)
    if user.exists():
        return user.get()
    return None


@sync_to_async
def get_user_from_payload(payload: dict):
    email = payload.get("sub")
    user = user_models.User.users.get_users().filter(email=email).distinct()
    user.update(is_active=True)
    return user.get()


@sync_to_async
def get_user_sync(**kwargs):
    user = user_models.User.objects.filter(**kwargs)
    if user.exists():
        return user.get()
    return
