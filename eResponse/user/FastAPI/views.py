import json
import logging

from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpRequest

from fastapi import Request, HTTPException
from .schemas import UserSchema

User = get_user_model()


@csrf_protect
@require_safe
@require_http_methods(["POST", "GET", "PUT"])
def users_view(request: Request):
    if request.method == "POST":
        pass


@csrf_protect
@require_http_methods(["POST", "GET"])
def create_user(request: HttpRequest) -> JsonResponse:
    """
    create user object with email and password
    flow: the user must activate account and complete other
    registration steps before full authorization is granted.
    :param request:
    :return: [JsonResponse]
    """
    try:
        if request.method == "POST":
            data: dict = json.loads(request.body)
            user: User = User.objects.create_user(**data)

            schema = UserSchema.from_django(user)
            return JsonResponse({'user': schema.dict()})

    except Exception as error:
        raise HTTPException(status_code=400)
        # return JsonResponse({"detail": str(error)}, status=status)



def get_respondent(request):
    pass


def update_respondent(request):
    pass


def add_certification(request):
    pass


def update_certification(request):
    pass


