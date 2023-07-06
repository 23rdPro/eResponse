from fastapi import APIRouter

from django.urls import path, re_path

from . import views


router = APIRouter()

router.get('/users')


urlpatterns = [
    path("/eer/users/", views.users_view, ),

]
