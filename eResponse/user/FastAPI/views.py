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
from typing import List, Dict, Coroutine, Union, Tuple, Annotated, Any, Optional


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
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# from eResponse.urls import router
from eResponse.user import models as user_models

from starlette.responses import PlainTextResponse, RedirectResponse

from eResponse.auth_token.FastAPI import schema as auth_token_schema

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema, UserRegistrationSchema
from eResponse import (
    oauth2_scheme,
    pwd_context,
    ALGORITHM,
    API_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES,
    PREFIX
)

from .utils import (
    create_access_token_sync, create_user_sync, get_user_from_token,
    authenticate_user, to_schema, get_all_users,
    filter_user_by_id, jwt_decode, update_user_sync, activate_user_sync,
    get_object_token, get_user_from_payload, get_user_sync
)

URL = ""



async def create_user(*, new_user: UserRegistrationSchema):
    user = await create_user_sync(**new_user.dict())
    token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token_sync({"sub": user.email}, expires_delta=token_expires)
    if user is not None:
        return RedirectResponse(url=f"{PREFIX}/users/{access_token}/activate")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect email or password")


async def activate_user(token: Optional[str]):
    if token and isinstance(token, str):
        payload = await jwt_decode(token)
        user = await get_user_from_payload(payload)
        return {"is_activated": user.is_active}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token not found")


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


async def logout(current_user: Depends(get_current_active_user)):
    pass


async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    _user_check = await get_user_sync(email=form.username)
    if _user_check and not _user_check.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    _user_authenticate = await authenticate_user(form.username, form.password)
    if _user_authenticate is None:
        raise http_exception

    token_expires = timedelta(minutes=int(LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token_sync({"sub": _user_authenticate.email}, expires_delta=token_expires)
    token_data = {"access_token": access_token, "user_id": str(_user_authenticate.id)}
    token_data.setdefault("token_type", "bearer")
    response_model = auth_token_schema.TokenModel(**token_data)

    return response_model


async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return await to_schema(current_user, UserSchema)


async def read_users():
    users = await get_all_users()
    return await to_schema(users, UserSchema)


async def get_user(user_id: str):
    user = await filter_user_by_id(user_id)
    if user is not None:
        return await to_schema(user, UserSchema)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


async def update_user(user: UserSchema, user_id: str):
    curr_user = await filter_user_by_id(user_id)
    schema = await sync_to_async(lambda: UserSchema.from_orm(curr_user))()
    update_data = await sync_to_async(lambda: user.dict(exclude_unset=True))()
    updated_user = await sync_to_async(lambda: schema.copy(update=update_data))()
    await update_user_sync(curr_user, updated_user)
    return updated_user


async def delete_user(*, user_id: str):
    user = await filter_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    # assert hasattr(user, 'delete')  test
    await sync_to_async(lambda: user.delete())()
    return {"ok": True}
