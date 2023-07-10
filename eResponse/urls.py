import typing
from django.contrib import admin, auth
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from fastapi import APIRouter, Depends
from . import oauth2_scheme
from eResponse.user import UserType
from eResponse.user.FastAPI import views, schemas
from eResponse.user import models

router = APIRouter()

router.get(
    '/users',
    # dependencies=[Depends(oauth2_scheme)],
    # responses={404: {"description": "Not found"}},
    # response_model=schemas.UsersSchema,
    tags=["users", "experts", ],
    summary="Retrieve all users",
    status_code=200,
)(views.read_users)

router.post(
    '/users',
    status_code=200,
    summary="Post to user"
)(views.create_user)
