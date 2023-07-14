import json
import logging
from rest_framework.authtoken.models import Token
import eResponse
import typing
import httpx
import uuid
import asyncio
from asgiref.sync import sync_to_async
from typing import List, Dict, Coroutine, Union, Tuple, Annotated

from djantic import ModelSchema

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

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema
from eResponse import oauth2_scheme


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
def get_user_by_token(token: str):
    user = user_models.User.users.get_users().filter(email=token)
    if user.exists():
        return user.get()
    return None


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],

):
    user = await get_user_by_token(token)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive User")


@sync_to_async
def authenticate_user(email: str, password: str):
    return authenticate(email=email, password=password)


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": user.email, "token_type": "bearer"}


@sync_to_async
def to_schema(model: models, schema: ModelSchema, many=False):
    if not many:
        return schema.from_orm(model)
    return schema.from_django(model, many=True)


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return await to_schema(current_user, UserSchema)


async def delete_user_me():
    pass
