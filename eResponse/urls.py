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

from eResponse.response.FastAPI.views import start_emergency_response, get_emergency_response


tags = ["users",]
router = APIRouter(tags=tags)

router.post("/token", status_code=status.HTTP_200_OK,
            summary="jwt login")(views.login)

router.get('/users', dependencies=[Depends(oauth2_scheme)],
           summary="retrieve all users",
           status_code=status.HTTP_200_OK)(views.read_users)

router.post('/users', status_code=status.HTTP_201_CREATED,
            summary="create user")(views.create_user)

router.get("/users/me", status_code=200, tags=["users", ]
           )(views.read_users_me)

router.get("/users/{user_id}", status_code=status.HTTP_200_OK)(views.get_user)

router.patch("/users/{user_id}", status_code=status.HTTP_200_OK)(views.update_user)

router.delete("/users/{user_id}", summary="delete current user",
              status_code=status.HTTP_204_NO_CONTENT,
              )(views.delete_user)

router.get("/response", status_code=status.HTTP_200_OK)(get_emergency_response)


urlpatterns = []
