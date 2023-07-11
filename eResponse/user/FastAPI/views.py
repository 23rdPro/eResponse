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

from fastapi import Request, HTTPException, Depends, FastAPI, Response, File
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    users = await sync_to_async(list)(models.User.users.get_experts().filter(id=token))
    assert len(users) == 1
    user = users.pop()
    try:
        user = models.User.objects.aget(user.id)
    except Exception as Error:
        logging.error(Error)
    finally:
        return await sync_to_async(lambda: {"user": UserSchema.from_orm(user)})()


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    return current_user
