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

from eResponse.auth_token.FastAPI import schema as auth_token_schema

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema, UserRegistrationSchema
from eResponse import oauth2_scheme, pwd_context, ALGORITHM, API_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

from .utils import (
    create_access_token, create_user_sync, get_user_from_token,
    authenticate_user, login_token_async, to_schema, get_all_users,
    filter_user_by_id, jwt_decode
)

URL = ""


async def create_user(*, new_user: UserRegistrationSchema):
    user = await create_user_sync(**new_user.dict())
    if user is not None:
        return new_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect email or password")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await jwt_decode(token)
        email: str = payload.get("sub")
        user = await get_user_from_token(email)
        if email is None or user is None:
            raise http_exception

    except JWTError:
        raise http_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(form.username, form.password)
    print("Here>>>>>>>>>>>>>>", user)
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


async def delete_user(*, curr_user: Annotated[UserSchema, Depends(get_current_user)], user_id: str):
    user = await filter_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    assert hasattr(user, 'delete')
    await sync_to_async(lambda: user.delete())()
    return

