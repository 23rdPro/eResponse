import typing
from django.contrib import admin, auth
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from fastapi import APIRouter, Depends, status
from . import oauth2_scheme
from eResponse.response import RESPONSE_PREFIX
from eResponse.user import UserType
from eResponse.user.FastAPI import views, schemas
from eResponse.user import models

from eResponse.response.FastAPI.views import (
    start_emergency_response,
    get_emergency_response,
    create_brief,
    upload_files,
)


router = APIRouter()

users = ["users"]
responses = ["responses"]

router.post("/token", status_code=status.HTTP_200_OK,
            summary="jwt login", tags=users)(views.login)

router.get('/users', dependencies=[Depends(oauth2_scheme)],
           summary="retrieve all users", tags=users,
           status_code=status.HTTP_200_OK)(views.read_users)

router.post('/users', status_code=status.HTTP_201_CREATED,
            summary="create user", tags=users)(views.create_user)

router.get("/users/me", status_code=200, tags=users,
           )(views.read_users_me)

# router.post("/users/me/activate", status_code=status.HTTP_200_OK, tags=users)(views.activate_user)

router.post("/users/{token}/activate", status_code=status.HTTP_200_OK, tags=users)(views.activate_user)

router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=users)(views.get_user)

router.patch("/users/{user_id}", status_code=status.HTTP_200_OK, tags=users)(views.update_user)

router.delete("/users/{user_id}", summary="delete current user",
              status_code=status.HTTP_204_NO_CONTENT, tags=users
              )(views.delete_user)

# router.get("/response", status_code=status.HTTP_200_OK)(get_emergency_response)

router.post(f"/{RESPONSE_PREFIX}/start-response", status_code=status.HTTP_201_CREATED, tags=responses)(start_emergency_response)
router.post("/%s/add-brief/{emergency_id}/{user_id}" % RESPONSE_PREFIX, status_code=status.HTTP_200_OK, tags=responses)(create_brief)
router.post("/%s/add-files/{emergency_id}" % RESPONSE_PREFIX, status_code=status.HTTP_200_OK, tags=responses)(upload_files)
# router.post("/upload-file", status_code=status.HTTP_200_OK, tags=responses)(upload_file)
# router.post("/ers-files/upload/file", )  # upload file


urlpatterns = []
