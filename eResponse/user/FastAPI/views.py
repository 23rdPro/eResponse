import json
import logging

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


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    user = await sync_to_async(models.User.users.get_users().filter(id=token))()

    try:
        user = models.User.objects.aget(user.id)
    except ObjectDoesNotExist or Exception as Error:
        logging.error(Error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    finally:
        return await sync_to_async(lambda: {
            "user": UserSchema.from_orm(user)})()


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    data: UserSchema = await sync_to_async(lambda: current_user)()
    if not sync_to_async(models.User.from_api(data).aget().is_active):
        raise HTTPException(status_code=400, detail="Inactive User")
    return data


@sync_to_async
def authenticate_user(email: str, password: str):
    return authenticate(email=email, password=password)


async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    form = await sync_to_async(lambda: form_data)()
    print(form.password)
    user = await authenticate_user(form.username, password=form.password)
    print(user)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": user.email, "token_type": "bearer"}


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return current_user
