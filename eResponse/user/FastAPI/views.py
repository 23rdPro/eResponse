import json
import eResponse
import typing
import httpx
import asyncio
from asgiref.sync import sync_to_async
from typing import List, Dict, Coroutine

from django.conf import settings
from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpRequest
from django.db import transaction

from fastapi import Request, HTTPException, Depends, FastAPI
# from eResponse.urls import router
from eResponse.user import models

from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema

# User = get_user_model()

URL = ""


async def read_users() -> Dict[str, List]:
    queryset: List = await sync_to_async(list)(
        models.User.users.get_users())

    return {"users": UserSchema.from_django(queryset, many=True)}


async def create_user(email, password):
    user = await models.User.objects.acreate(email=email, password=password)
    return UserSchema.from_orm(user)


# # @router.get("")
# def read_managers():
#     queryset = User.users.get_managers()
#
#
# # @router.get("")
# def read_experts():
#     queryset = User.users.get_experts()
#
#
# # @router.get("")
# def read_leads():
#     queryset = User.users.get_leads()
#
#
# @csrf_protect
# @require_safe
# @require_http_methods(["POST", "GET", "PUT"])
# def users_view(request: Request):
#     if request.method == "POST":
#         pass
#
#
# @csrf_protect
# @require_http_methods(["POST", "GET"])
# def create_user(request: HttpRequest) -> JsonResponse:
#     """
#     create user object with email and password
#     flow: the user must activate account and complete other
#     registration steps before full authorization is granted.
#     :param request:
#     :return: [JsonResponse]
#     """
#     try:
#         if request.method == "POST":
#             data: dict = json.loads(request.body)
#             user: User = User.objects.create_user(**data)
#
#             schema = eResponse.user.FastAPI.schemas.UserSchema.from_django(user)
#             return JsonResponse({'user': schema.dict()})
#
#     except Exception as error:
#         raise HTTPException(status_code=400)
#         # return JsonResponse({"detail": str(error)}, status=status)
#
#
#
# def get_respondent(request):
#     pass
#
#
# def update_respondent(request):
#     pass
#
#
# def add_certification(request):
#     pass
#
#
# def update_certification(request):
#     pass
#
#
