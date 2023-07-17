import typing
from django.contrib import admin, auth
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from fastapi import APIRouter, Depends, status
from . import oauth2_scheme
from eResponse.user import UserType
from eResponse.user.FastAPI import views, schemas
from eResponse.user import models

router = APIRouter()

users = ["users"]

router.get('/users', dependencies=[Depends(oauth2_scheme)],
           tags=["users", ], summary="Retrieve all users",
           status_code=200)(views.read_users)

router.post('/users', tags=["users", ], status_code=200,
            summary="Post to user")(views.create_user)

router.post("/token", status_code=200, tags=["users"])(views.login)

router.get("/users/me", status_code=200, tags=["users", ]
           )(views.read_users_me)

router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=users
           )(views.get_user)


urlpatterns = []
