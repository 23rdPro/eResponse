from __future__ import annotations

import json
import logging
from datetime import timedelta, datetime

from rest_framework.authtoken.models import Token
import eResponse
import os
import typing
import httpx
import uuid
import asyncio
from asgiref.sync import sync_to_async
from typing import List, Dict, Coroutine, Union, Tuple, Annotated, Any


from djantic import ModelSchema
from jose import jwt, JWTError


from django.conf import settings
from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpRequest
from django.db import transaction, models
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as user_login

from fastapi import Request, HTTPException, Depends, FastAPI, Response, File, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# from eResponse.urls import router
from eResponse.user import models as user_models
from eResponse.auth_token import models as auth_token_models
from eResponse.auth_token.FastAPI import schema as auth_token_schema

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema
from eResponse import oauth2_scheme, pwd_context, ALGORITHM, API_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

from .utils import create_access_token

URL = ""


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
def authenticate_user(email: str, password: str):
    return authenticate(email=email, password=password)


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
def login_token_async(user, access_token):
    auth_token = auth_token_models.Token.objects.select_related("user").filter(user=user.id)
    if auth_token.exists():
        auth_token.update(access_token=access_token)
        return auth_token.get()
    return auth_token_models.Token.objects.create(access_token=access_token, user=user)


@sync_to_async
def get_user(**kwargs):
    user = user_models.User.objects.filter(**kwargs)
    if user.exists():
        return user.get()
    return


async def create_user(user: UserSchema):
    await from_schema(user_models.User, user)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await sync_to_async(lambda: jwt.decode(token, API_SECRET_KEY, algorithms=[ALGORITHM]))()
        email: str = payload.get("sub")
        if email is None:
            raise http_exception
    except JWTError:
        raise http_exception

    user = await get_user_from_token(email)
    if user is None:
        raise http_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive User")


CurrentActiveUser = Annotated[UserSchema, Depends(get_current_active_user)]


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(form.username, form.password)
    if user is None:
        raise http_exception

    token_expires = await sync_to_async(lambda: timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))()
    access_token = await create_access_token({"sub": user.email}, expires_delta=token_expires)

    auth_token = await login_token_async(user, access_token)

    return await to_schema(auth_token, auth_token_schema.TokenSchema)


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return await to_schema(current_user, UserSchema)


async def read_users():
    users = await get_all_users()
    return await to_schema(users, UserSchema)


async def get_user_by_id(user_id: str):
    user = await filter_user_by_id(user_id)
    if user is not None:
        return await to_schema(user, UserSchema)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


async def update_user(user: UserSchema, user_id: str):
    return user


async def delete_user(*, user: CurrentActiveUser, ):
    pass
