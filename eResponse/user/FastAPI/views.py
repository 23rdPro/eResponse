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
from typing import List, Dict, Coroutine, Union, Tuple, Annotated


from djantic import ModelSchema
from jose import jwt, JWTError


from django.conf import settings
from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpRequest
from django.db import transaction, models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as user_login

from fastapi import Request, HTTPException, Depends, FastAPI, Response, File, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# from eResponse.urls import router
from eResponse.user import models as user_models
from eResponse.auth_token import models as auth_token_models
from eResponse.auth_token.FastAPI import schema as auth_token_schema

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema
from eResponse import oauth2_scheme, pwd_context, ALGORITHM, API_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

from .utils import create_access_token

URL = ""


async def read_users() -> Dict[str, List]:
    queryset: Union[Tuple, Coroutine] = await sync_to_async(tuple)(
        user_models.User.users.get_users())

    return await sync_to_async(lambda: {
        "users": UserSchema.from_django(queryset, many=True)})()


async def create_user(schema_type: UserSchema) -> UserSchema:
    data: UserSchema = await sync_to_async(lambda: schema_type)()
    await sync_to_async(lambda: user_models.User.from_api(data).save())()
    return data


@sync_to_async
def get_user_from_token(token: str):
    user = user_models.User.users.get_users().filter(email=token)
    if user.exists():
        return user.aget()
    return None


@sync_to_async
def get_payload(token, secret, algorithms=None):
    pass


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = None
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload>>>>>>>>>>>>>>:{0}".format(payload))
        email = payload.get("sub")
        print(email)
        user = await get_user_from_token(email)
        if email is None or user is None:
            raise http_exception

    except JWTError or Exception as Err:
        print("Error>>>>>>>>", Err)
        raise http_exception
    finally:
        return user

    # user = await get_user_from_token(email)
    # if user is not None:
    #     return user
    #
    # raise http_exception


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive User")


@sync_to_async
def authenticate_user(email: str, password: str):
    return authenticate(email=email, password=password)


@sync_to_async
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@sync_to_async
def to_schema(model: models, schema: ModelSchema, many=False):
    return schema.from_orm(model) if not many else \
        schema.from_django(model, many=True)


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
    # token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token({"sub": user.email}, expires_delta=token_expires)

    auth_token = await sync_to_async(lambda: auth_token_models.Token.objects.select_related("user").filter(user=user.id))()
    if await auth_token.aexists():
        await auth_token.aupdate(access_token=access_token)
    else:
        auth_token = await sync_to_async(lambda: auth_token_models.Token.objects.create(access_token=access_token, user=user))()
    # print(auth_token, "auth_token>>>>>>>>>>>")
    return await to_schema(auth_token, auth_token_schema.TokenSchema)


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return await to_schema(current_user, UserSchema)
