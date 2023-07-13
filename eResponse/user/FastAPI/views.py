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

from django.conf import settings
from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpRequest
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as user_login

from fastapi import Request, HTTPException, Depends, FastAPI, Response, File, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# from eResponse.urls import router
from eResponse.user import models

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema
from eResponse import oauth2_scheme

# User = get_user_model()

URL = ""


async def read_users() -> Dict[str, List]:
    queryset: Union[Tuple, Coroutine] = await sync_to_async(tuple)(
        models.User.users.get_users())

    return await sync_to_async(lambda: {
        "users": UserSchema.from_django(queryset, many=True)})()


async def create_user(schema_type: UserSchema) -> UserSchema:
    data: UserSchema = await sync_to_async(lambda: schema_type)()
    await sync_to_async(lambda: models.User.from_api(data).save())()
    return data


@sync_to_async
def get_user_by_token(token: str):
    return models.User.users.get_users().filter(id=token)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],

):
    user = await get_user_by_token(token)

    if user.exists():
        return await user.aget()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

    # data: UserSchema = await sync_to_async(lambda: current_user)()
    # if not sync_to_async(models.User.from_api(data).aget().is_active):
    #     raise HTTPException(status_code=400, detail="Inactive User")
    # return data


@sync_to_async
def authenticate_user(email: str, password: str):
    return authenticate(email=email, password=password)


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": user.email, "token_type": "bearer"}


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return current_user


async def delete_user_me():
    pass
