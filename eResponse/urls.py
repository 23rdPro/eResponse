import typing
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from fastapi import APIRouter, Depends

from . import oauth2_scheme

router = APIRouter()

router.get(
    '/users',
    dependencies=[Depends(oauth2_scheme)],
    # responses={404: {"description": "Not found"}},
)


urlpatterns = [
    # path('', admin.site.urls),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
